import React, { useEffect, useState } from 'react'
import { Link, Outlet, useParams } from 'react-router-dom'

const THEMES: Record<string, { title: string; color: string }> = {
    A: { title: '学院 A 选课系统', color: '#2563eb' },
    B: { title: '学院 B 选课系统', color: '#10b981' },
    C: { title: '学院 C 选课系统', color: '#f97316' }
}

function normalizeCollegeId(value: string | undefined) {
    if (!value) return 'A'
    const upper = value.toUpperCase()
    return ['A', 'B', 'C'].includes(upper) ? upper : 'A'
}

export default function CollegeLayout() {
    const { collegeId } = useParams()
    const resolvedId = normalizeCollegeId(collegeId)
    const theme = THEMES[resolvedId]
    const [name, setName] = useState(sessionStorage.getItem('name'))

    useEffect(() => {
        document.documentElement.style.setProperty('--theme', theme.color)
    }, [theme.color])

    // 监听 collegeId 变化，如果变化则清除登陆状态
    useEffect(() => {
        const lastCollegeId = sessionStorage.getItem('lastCollegeId')
        if (lastCollegeId && lastCollegeId !== resolvedId) {
            // 学院 ID 变化，清除登陆状态
            sessionStorage.removeItem('sid')
            sessionStorage.removeItem('name')
            setName(null)
        }
        sessionStorage.setItem('lastCollegeId', resolvedId)
    }, [resolvedId])

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100">
            <header className="sticky top-0 z-20 border-b border-white/10 bg-slate-950/80 backdrop-blur">
                <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-3">
                        <div
                            className="h-10 w-10 rounded-2xl shadow-lg"
                            style={{ background: `linear-gradient(135deg, ${theme.color}, #0f172a)` }}
                        />
                        <div>
                            <div className="text-lg font-semibold text-white">{theme.title}</div>
                            <div className="text-xs uppercase tracking-[0.2em] text-slate-500">EduIntegrate</div>
                        </div>
                    </div>
                    <nav className="flex items-center gap-6 text-sm">
                        <Link className="text-slate-300 hover:text-white" to={`/college/${resolvedId}`}>首页</Link>
                        <Link className="text-slate-300 hover:text-white" to={`/college/${resolvedId}/courses`}>课程</Link>
                        <Link className="text-slate-300 hover:text-white" to={`/college/${resolvedId}/enrollments`}>我的选课</Link>
                        {name ? (
                            <Link className="text-slate-300 hover:text-white" to={`/college/${resolvedId}/login`}>切换用户</Link>
                        ) : (
                            <Link className="text-slate-300 hover:text-white" to={`/college/${resolvedId}/login`}>登录</Link>
                        )}
                    </nav>
                    <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs font-semibold text-slate-200">
                        {name ? name : '访客'}
                    </div>
                </div>
            </header>
            <main className="mx-auto w-full max-w-6xl px-6 pb-16 pt-8">
                <Outlet />
            </main>
        </div>
    )
}
