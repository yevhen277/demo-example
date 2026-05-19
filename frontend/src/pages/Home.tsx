import React from 'react'
import { Link, useParams } from 'react-router-dom'
import { BookOpen, Globe, ClipboardList, ArrowRight, User, Lock } from 'lucide-react'

const THEMES: Record<string, { title: string; color: string; gradient: string; greeting: string }> = {
    A: { title: '学院 A 选课系统', color: '#2563eb', gradient: 'from-blue-600 to-blue-900', greeting: '欢迎来到学院 A' },
    B: { title: '学院 B 选课系统', color: '#10b981', gradient: 'from-emerald-600 to-emerald-900', greeting: '欢迎来到学院 B' },
    C: { title: '学院 C 选课系统', color: '#f97316', gradient: 'from-orange-600 to-orange-900', greeting: '欢迎来到学院 C' }
}

function normalizeCollegeId(value: string | undefined) {
    if (!value) return 'A'
    const upper = value.toUpperCase()
    return ['A', 'B', 'C'].includes(upper) ? upper : 'A'
}

export default function Home() {
    const { collegeId } = useParams()
    const resolvedId = normalizeCollegeId(collegeId)
    const theme = THEMES[resolvedId]
    const name = sessionStorage.getItem('name')
    const sid = sessionStorage.getItem('sid')
    const isLoggedIn = !!name

    return (
        <div className="space-y-10">
            <div className={`relative overflow-hidden rounded-[28px] bg-gradient-to-br ${theme.gradient} p-10 shadow-2xl`}
                style={{ boxShadow: '0 25px 80px rgba(15, 23, 42, 0.55)' }}
            >
                <div className="absolute inset-0 bg-black/25" />
                <div className="absolute -bottom-24 -right-20 h-72 w-72 rounded-full bg-white/10 blur-3xl" />
                <div className="absolute -top-20 -left-10 h-48 w-48 rounded-full bg-white/10 blur-2xl" />

                <div className="relative z-10 max-w-2xl space-y-6">
                    <div className="flex items-center gap-3">
                        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/20 backdrop-blur">
                            <BookOpen className="h-6 w-6 text-white" />
                        </div>
                        <div>
                            <div className="text-sm uppercase tracking-[0.3em] text-white/70">EduIntegrate</div>
                            <h1 className="text-3xl font-bold text-white">{theme.title}</h1>
                            <p className="text-sm text-white/70">异构数据库集成 · 统一 XML Schema 交换</p>
                        </div>
                    </div>

                    {isLoggedIn ? (
                        <div className="inline-flex items-center gap-3 rounded-2xl bg-white/15 px-5 py-3 text-white shadow-lg">
                            <User className="h-4 w-4" />
                            <span className="font-semibold">你好，{name}</span>
                            <span className="text-white/70">（{sid}）</span>
                            <span className="text-white/50">|</span>
                            <span className="text-sm text-white/80">已登录，可直接选课</span>
                        </div>
                    ) : (
                        <div className="inline-flex items-center gap-2 rounded-2xl bg-white/10 px-4 py-2 text-sm text-white/70">
                            <Lock className="h-4 w-4" />
                            登录后可进行选课、退课等操作
                        </div>
                    )}

                    <div className="flex flex-wrap gap-4">
                        <Link
                            to={`/college/${resolvedId}/courses`}
                            className="inline-flex items-center gap-2 rounded-xl bg-white px-6 py-3 text-sm font-semibold text-slate-900 transition hover:-translate-y-0.5 hover:bg-slate-100"
                        >
                            进入选课
                            <ArrowRight className="h-4 w-4" />
                        </Link>
                        {!isLoggedIn && (
                            <Link
                                to={`/college/${resolvedId}/login`}
                                className="inline-flex items-center gap-2 rounded-xl border border-white/40 bg-white/10 px-6 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-white/20"
                            >
                                登录
                            </Link>
                        )}
                    </div>
                </div>
            </div>

            {/* 功能卡片 */}
            <div className="grid gap-6 md:grid-cols-3">

                <Link to={`/college/${resolvedId}/courses?tab=local`} className="group rounded-2xl border border-slate-800 bg-slate-900/70 p-6 transition-all duration-300 hover:-translate-y-2 hover:border-slate-700 hover:shadow-xl hover:shadow-blue-900/20">
                    <div className="w-12 h-12 rounded-xl bg-blue-600/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                        <BookOpen className="w-6 h-6 text-blue-400" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-100 mb-2">本院课程</h3>
                    <p className="text-slate-400 text-sm mb-4">查看并选修本院开设的所有课程，涵盖各专业核心课程</p>
                    <div className="flex items-center gap-2 text-blue-400 text-sm font-semibold group-hover:text-blue-300">
                        查看课程 <ArrowRight className="w-4 h-4" />
                    </div>
                </Link>

                <Link to={`/college/${resolvedId}/courses?tab=shared`} className="group rounded-2xl border border-slate-800 bg-slate-900/70 p-6 transition-all duration-300 hover:-translate-y-2 hover:border-slate-700 hover:shadow-xl hover:shadow-emerald-900/20">
                    <div className="w-12 h-12 rounded-xl bg-emerald-600/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                        <Globe className="w-6 h-6 text-emerald-400" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-100 mb-2">共享课程</h3>
                    <p className="text-slate-400 text-sm mb-4">跨院选修其他学院的开放课程，拓宽学习视野，探索跨学科领域</p>
                    <div className="flex items-center gap-2 text-emerald-400 text-sm font-semibold group-hover:text-emerald-300">
                        查看课程 <ArrowRight className="w-4 h-4" />
                    </div>
                </Link>

                <Link to={`/college/${resolvedId}/enrollments`} className="group rounded-2xl border border-slate-800 bg-slate-900/70 p-6 transition-all duration-300 hover:-translate-y-2 hover:border-slate-700 hover:shadow-xl hover:shadow-orange-900/20">
                    <div className="w-12 h-12 rounded-xl bg-orange-600/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                        <ClipboardList className="w-6 h-6 text-orange-400" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-100 mb-2">我的选课</h3>
                    <p className="text-slate-400 text-sm mb-4">查看已选课程，进行退课操作，管理个人课表</p>
                    <div className="flex items-center gap-2 text-orange-400 text-sm font-semibold group-hover:text-orange-300">
                        查看详情 <ArrowRight className="w-4 h-4" />
                    </div>
                </Link>

            </div>

            {/* 底部提示 */}
            <div className="text-center text-sm text-slate-500">
                <p>基于 XML Schema 统一交换 · 三院异构数据库互联互通</p>
            </div>
        </div>
    )
}