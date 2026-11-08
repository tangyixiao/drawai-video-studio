import React from 'react'
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion'
import { DUST, FIELD, INK, PAPER, SERIF, SANS, STAMP, SURFACE } from './theme'

const ease = Easing.bezier(0.2, 0.8, 0.2, 1)
const unit = (f: number, start: number, end: number) => interpolate(f, [start, end], [0, 1], { easing: ease, extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
// Deterministic SVG grain, using the upstream scene-kit's paper dither technique.
const grain = 'data:image/svg+xml;utf8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7"/><feColorMatrix type="saturate" values="0"/></filter><rect width="160" height="160" filter="url(#n)"/></svg>')

function Marks() {
  return <>{[[22, 22], [610, 22], [22, 390], [610, 390]].map(([x, y], i) => <svg key={i} style={{ position: 'absolute', left: x - 13, top: y - 13, width: 26, height: 26, overflow: 'visible' }}>
    <path d="M0 13H26M13 0V26" fill="none" stroke={DUST} strokeWidth="0.8" />
  </svg>)}</>
}

function Sheet({ level, frame }: { level: number; frame: number }) {
  const entrance = unit(frame, 16 + level * 12, 56 + level * 12)
  const top = [478, 294, 95][level]
  const angle = [-7, -10, -13][level]
  return <div style={{ position: 'absolute', left: 837 + (2 - level) * 34, top: top + (1 - entrance) * 145,
    width: 636, height: 416, opacity: entrance * (0.59 + level * 0.19), zIndex: level,
    transform: `perspective(1700px) rotateY(-17deg) rotateX(8deg) rotateZ(${angle + (1 - entrance) * 9}deg)`,
    transformOrigin: '20% 50%', background: SURFACE, border: '1px solid rgba(255,255,255,.9)',
    boxShadow: '15px 32px 55px rgba(51,58,78,.14), 0 2px 7px rgba(45,48,65,.06)', padding: 43 }}>
    <Marks />
    <div style={{ position: 'relative', width: 550, height: 310, overflow: 'hidden', border: `1px solid ${INK}`, background: FIELD }}>
      <Img src={staticFile('storyboard-illustration.png')} style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: level === 2 ? .88 : .52,
        objectPosition: level === 0 ? '8% center' : 'center', transform: `scale(${level === 0 ? 1.55 : 1})`, filter: 'grayscale(1)' }} />
      <div style={{ position: 'absolute', inset: 0, background: `linear-gradient(110deg,${SURFACE}22,transparent 70%)` }} />
    </div>
    <div style={{ position: 'absolute', bottom: 18, left: 44, right: 44, display: 'flex', justifyContent: 'space-between', fontFamily: SANS, fontSize: 10, letterSpacing: 2, color: DUST }}>
      <span>DRAWAI / SCENE 0{3 - level}</span><span>STORYBOARD STUDY</span>
    </div>
  </div>
}

export default function Scene() {
  const frame = useCurrentFrame()
  const { width, durationInFrames } = useVideoConfig()
  const end = unit(frame, 105, durationInFrames - 1)
  return <AbsoluteFill style={{ background: PAPER, overflow: 'hidden', color: INK }}>
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 18% 12%,${SURFACE},transparent 58%),linear-gradient(130deg,transparent 45%,${FIELD})` }} />
    <AbsoluteFill style={{ backgroundImage: `url("${grain}")`, backgroundSize: '160px 160px', opacity: .055, mixBlendMode: 'multiply' }} />
    <div style={{ position: 'absolute', width: 1000, height: 280, left: 510, top: 593, background: 'rgba(68,77,101,.09)', filter: 'blur(42px)', transform: 'rotate(-10deg)' }} />
    <div style={{ position: 'absolute', inset: 0, transform: `translateX(${-end * 8}px) scale(${1 + end * .008})`, transformOrigin: '75% 45%' }}>
      {[0, 1, 2].map(level => <Sheet key={level} level={level} frame={frame} />)}
    </div>
    <div style={{ position: 'absolute', top: 43, left: 74, opacity: unit(frame, 0, 18), fontFamily: SANS, fontSize: 14, letterSpacing: 3.5, color: DUST }}>DrawAI / MOTION STUDIES</div>
    <div style={{ position: 'absolute', left: 72, top: 149, width: width * .52, fontFamily: SERIF, fontWeight: 900, letterSpacing: -3 }}>
      {[['让分镜', 112, 4], ['变成可编辑的', 82, 14], ['视频', 142, 25]].map(([text, size, start], i) => {
        const show = unit(frame, Number(start), Number(start) + 24)
        return <div key={i} style={{ position: 'relative', width: '100%', height: [138, 113, 172][i], opacity: show, transform: `translateY(${(1 - show) * 30}px)`, fontSize: Number(size), lineHeight: 1.08 }}>{text}</div>
      })}
      <svg style={{ position: 'absolute', left: 279, top: 108, width: 72, height: 31, transform: 'rotate(-11deg)' }}>
        <ellipse cx="36" cy="15" rx="31" ry="10" fill="none" stroke={STAMP} strokeWidth="2.6" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - unit(frame, 80, 112)} />
      </svg>
    </div>
    <div style={{ position: 'absolute', left: 76, bottom: 100, opacity: unit(frame, 48, 73), fontFamily: SANS, fontSize: 29, letterSpacing: 6, color: DUST }}>分镜 / 场景 / 成片</div>
    <div style={{ position: 'absolute', left: 76, bottom: 44, opacity: unit(frame, 69, 91), fontFamily: SANS, fontSize: 12, letterSpacing: 2, color: DUST }}>01 — PAPER STORYBOARD</div>
  </AbsoluteFill>
}
