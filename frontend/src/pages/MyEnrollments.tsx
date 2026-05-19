import React, { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchMyEnrollments, withdrawEnrollment } from '../api'

export default function MyEnrollments() {
    const [list, setList] = useState<any[]>([])
    const [msg, setMsg] = useState('')
    const sid = sessionStorage.getItem('sid')
    const { collegeId } = useParams()
    const resolvedCollegeId = collegeId ? collegeId.toUpperCase() : 'A'

    useEffect(() => {
        if (!sid) return
        fetchMyEnrollments(sid).then(data => setList(data || []))
    }, [sid])

    async function withdraw(enrollmentId: string) {
        setMsg('退选中...')
        const res: any = await withdrawEnrollment(enrollmentId)
        if (res.code === 0) {
            setMsg('退选成功')
            setList(list.filter(i => i.enrollmentId !== enrollmentId))
        } else setMsg(`${res.code}: ${res.message}`)
    }

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-semibold text-white">我的选课</h2>
                <p className="text-sm text-slate-400">查看已选课程与退选状态</p>
            </div>
            {!sid && (
                <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300">
                    当前为游客模式，无法查看我的选课，请先 <Link className="text-white underline" to={`/college/${resolvedCollegeId}/login`}>登录</Link>。
                </div>
            )}
            {msg && (
                <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200">
                    {msg}
                </div>
            )}
            {sid && (
                <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60">
                    <div className="overflow-x-auto">
                        <table className="min-w-full text-sm">
                            <thead className="bg-slate-900/80 text-left text-xs uppercase tracking-widest text-slate-500">
                                <tr>
                                    <th className="px-4 py-3">报名号</th>
                                    <th className="px-4 py-3">课程号</th>
                                    <th className="px-4 py-3">名称</th>
                                    <th className="px-4 py-3">状态</th>
                                    <th className="px-4 py-3">操作</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {list.map(i => (
                                    <tr key={i.enrollmentId} className="hover:bg-white/5">
                                        <td className="px-4 py-3 font-mono text-xs text-slate-400">{i.enrollmentId}</td>
                                        <td className="px-4 py-3 text-slate-300">{i.cid}</td>
                                        <td className="px-4 py-3 text-white">{i.name}</td>
                                        <td className="px-4 py-3">
                                            <span className="rounded-full bg-white/5 px-3 py-1 text-xs font-semibold text-slate-300">
                                                {i.status}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3">
                                            <button
                                                onClick={() => withdraw(i.enrollmentId)}
                                                className="rounded-full border border-rose-500/40 px-4 py-2 text-xs font-semibold text-rose-300 transition hover:bg-rose-500/10"
                                            >
                                                退选
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    )
}
