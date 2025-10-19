---
theme: default
title: AI Presentation Generator
info: |
  ## AI Presentation Generator
  Transform your ideas into stunning presentations with AI
drawings:
  persist: false
transition: slide-left
mdc: true
---

<div v-motion
  :initial="{ y: -40, opacity: 0 }"
  :enter="{ y: 0, opacity: 1, transition: { delay: 200 } }">
  <h1 class="text-6xl font-bold text-purple-600">AI Transforms Presentations</h1>
</div>

<div v-motion
  :initial="{ y: 40, opacity: 0 }"
  :enter="{ y: 0, opacity: 1, transition: { delay: 500 } }">
  <p class="text-2xl mt-4 text-gray-600">From hours to minutes. From stress to success.</p>
</div>

<div v-motion
  :initial="{ scale: 0 }"
  :enter="{ scale: 1, transition: { delay: 800 } }"
  class="mt-8">
  <div class="text-4xl">✨</div>
</div>

<div v-motion
  :initial="{ opacity: 0 }"
  :enter="{ opacity: 1, transition: { delay: 1000 } }"
  class="mt-6">
  <p class="text-lg text-white opacity-80">by Daren, Nitya, Nadia, and Siri</p>
</div>

<div style="position: fixed; bottom: 0; left: 0; right: 0; background: rgba(30, 30, 30, 0.9); padding: 0.5rem 0; text-align: center; z-index: 100; backdrop-filter: blur(10px);">
  <span style="color: white; font-size: 0.9rem; font-weight: 500;">🚇 Subway Slides</span>
</div>

<style>
.slidev-layout {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
h1 {
  color: white !important;
}
p {
  color: rgba(255, 255, 255, 0.9) !important;
}
</style>

---
layout: two-cols
---

# ✨ Magical Features

<div v-click style="display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;">
  <div style="font-size: 1.8rem;">⚡</div>
  <div>
    <h3 style="font-weight: bold;">Instant Generation</h3>
    <p style="font-size: 0.875rem; opacity: 0.75;">Create full presentations in seconds</p>
  </div>
</div>

<div v-click="2" style="display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;">
  <div style="font-size: 1.8rem;">🎨</div>
  <div>
    <h3 style="font-weight: bold;">Smart Design</h3>
    <p style="font-size: 0.875rem; opacity: 0.75;">AI selects perfect layouts & colors</p>
  </div>
</div>

<div v-click="3" style="display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;">
  <div style="font-size: 1.8rem;">📊</div>
  <div>
    <h3 style="font-weight: bold;">Data Visualization</h3>
    <p style="font-size: 0.875rem; opacity: 0.75;">Auto-generate charts from your data</p>
  </div>
</div>

::right::

<div v-click="4" style="display: flex; justify-content: center; align-items: center; height: 100%;">
  <div v-motion
    :initial="{ rotate: -10, scale: 0.8 }"
    :enter="{ rotate: 0, scale: 1 }"
    style="position: relative;">
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to right, #60A5FA, #9333EA); filter: blur(20px); opacity: 0.5;"></div>
    <div style="position: relative; background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
      <div style="font-size: 4rem; margin-bottom: 1rem; text-align: center;">🤖</div>
      <p style="text-align: center; font-family: monospace;">AI-Powered</p>
    </div>
  </div>
</div>

<style>
.slidev-layout {
  background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
}
</style>

---
layout: fact
---

<div class="grid grid-cols-3 gap-8">
  <div v-click v-motion
    :initial="{ scale: 0 }"
    :enter="{ scale: 1 }"
    class="text-center">
    <div class="text-5xl font-bold text-white">95%</div>
    <div class="text-lg mt-2 text-white opacity-90">Time Saved</div>
  </div>

  <div v-click="2" v-motion
    :initial="{ scale: 0 }"
    :enter="{ scale: 1 }"
    class="text-center">
    <div class="text-5xl font-bold text-white">10x</div>
    <div class="text-lg mt-2 text-white opacity-90">Faster Creation</div>
  </div>

  <div v-click="3" v-motion
    :initial="{ scale: 0 }"
    :enter="{ scale: 1 }"
    class="text-center">
    <div class="text-5xl font-bold text-white">∞</div>
    <div class="text-lg mt-2 text-white opacity-90">Possibilities</div>
  </div>
</div>

<div v-click="4" class="text-center mt-12 text-2xl font-light">
  <span class="text-white opacity-90">Transform your ideas into stunning presentations</span>
</div>

<style>
.slidev-layout {
  background: linear-gradient(45deg, #FC466B 0%, #3F5EFB 100%);
}
</style>

---

# 🚀 Three Steps to Amazing

<div class="mt-8">

  <div v-click v-motion
    :initial="{ x: -100, opacity: 0 }"
    :enter="{ x: 0, opacity: 1 }"
    class="flex items-center gap-4 mb-6 bg-white bg-opacity-10 p-4 rounded-lg backdrop-blur">
    <div class="text-4xl font-bold text-pink-200">1</div>
    <div class="flex-1">
      <h3 class="text-xl font-bold text-white">Input Your Topic</h3>
      <p class="text-white opacity-90">Just tell our AI what you want to present</p>
    </div>
    <div class="text-3xl">📝</div>
  </div>

  <div v-click="2" v-motion
    :initial="{ x: -100, opacity: 0 }"
    :enter="{ x: 0, opacity: 1 }"
    class="flex items-center gap-4 mb-6 bg-white bg-opacity-10 p-4 rounded-lg backdrop-blur">
    <div class="text-4xl font-bold text-pink-200">2</div>
    <div class="flex-1">
      <h3 class="text-xl font-bold text-white">AI Works Its Magic</h3>
      <p class="text-white opacity-90">Advanced algorithms create perfect slides</p>
    </div>
    <div class="text-3xl">🤖</div>
  </div>

  <div v-click="3" v-motion
    :initial="{ x: -100, opacity: 0 }"
    :enter="{ x: 0, opacity: 1 }"
    class="flex items-center gap-4 mb-6 bg-white bg-opacity-10 p-4 rounded-lg backdrop-blur">
    <div class="text-4xl font-bold text-pink-200">3</div>
    <div class="flex-1">
      <h3 class="text-xl font-bold text-white">Present with Confidence</h3>
      <p class="text-white opacity-90">Download, customize, and wow your audience</p>
    </div>
    <div class="text-3xl">🎯</div>
  </div>

</div>

<div v-click="4" class="text-center mt-8">
  <span class="text-xl text-white opacity-90">⏱️ Total time: Under 2 minutes</span>
</div>

<style>
.slidev-layout {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}
</style>

---
layout: two-cols
---

# 🔋 We Love Red Bull

<div v-click v-motion
  :initial="{ y: 20, opacity: 0 }"
  :enter="{ y: 0, opacity: 1 }"
  style="margin-bottom: 1.5rem; padding: 1.2rem; background: rgba(255,255,255,0.1); border-radius: 12px; backdrop-filter: blur(10px);">
  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
    <span style="font-size: 2rem;">⚡</span>
    <h3 style="font-size: 1.3rem; font-weight: bold; color: white;">Fueling Innovation</h3>
  </div>
  <p style="color: rgba(255,255,255,0.9);">Red Bull kept our energy high and ideas flowing throughout the entire hackathon</p>
</div>

<div v-click="2" v-motion
  :initial="{ y: 20, opacity: 0 }"
  :enter="{ y: 0, opacity: 1 }"
  style="margin-bottom: 1.5rem; padding: 1.2rem; background: rgba(255,255,255,0.1); border-radius: 12px; backdrop-filter: blur(10px);">
  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
    <span style="font-size: 2rem;">🚀</span>
    <h3 style="font-size: 1.3rem; font-weight: bold; color: white;">Wings for Our Code</h3>
  </div>
  <p style="color: rgba(255,255,255,0.9);">Every can gave us wings to push through challenges and debug with clarity</p>
</div>

<div v-click="3" v-motion
  :initial="{ y: 20, opacity: 0 }"
  :enter="{ y: 0, opacity: 1 }"
  style="margin-bottom: 1.5rem; padding: 1.2rem; background: rgba(255,255,255,0.1); border-radius: 12px; backdrop-filter: blur(10px);">
  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
    <span style="font-size: 2rem;">💙</span>
    <h3 style="font-size: 1.3rem; font-weight: bold; color: white;">Hackathon MVP</h3>
  </div>
  <p style="color: rgba(255,255,255,0.9);">The real MVP of Reality Hackathon - powering late-night coding sessions</p>
</div>

<div v-click="5" style="margin-top: 2rem;">
  <p style="font-size: 1.1rem; color: rgba(255,255,255,0.9); font-weight: 500;">
    🙏 Special thanks to Red Bull for being an incredible hackathon sponsor!
  </p>
</div>

::right::

<div style="display: flex; align-items: center; justify-content: center; height: 100%;">
  <div v-click="4" v-motion
    :initial="{ scale: 0.3, rotate: -15 }"
    :enter="{ scale: 1, rotate: 5, transition: { type: 'spring', stiffness: 200 } }"
    style="position: relative;">
    <div style="position: absolute; inset: -20px; background: radial-gradient(circle, rgba(255,215,0,0.3), transparent); filter: blur(30px); animation: pulse 2s infinite;"></div>
    <div style="position: relative; background: linear-gradient(135deg, #1e3c72, #2a5298); padding: 3rem 2rem; border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); border: 2px solid rgba(255,255,255,0.2);">
      <div style="text-align: center;">
        <div style="font-size: 5rem; margin-bottom: 1rem; filter: drop-shadow(0 0 20px rgba(255,215,0,0.5));">⚡</div>
        <p style="font-size: 1.8rem; font-weight: bold; color: #FFD700; text-shadow: 0 0 20px rgba(255,215,0,0.5);">Red Bull</p>
        <p style="font-size: 1rem; color: white; margin-top: 0.5rem; font-style: italic;">Gives You Wings!</p>
      </div>
    </div>
  </div>
</div>

<style>
.slidev-layout {
  background: linear-gradient(135deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%);
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}
</style>

---
layout: center
---

<div v-motion
  :initial="{ y: -30, opacity: 0 }"
  :enter="{ y: 0, opacity: 1 }">
  <h1 class="text-5xl font-bold mb-8 text-white">Ready to Revolutionize Your Presentations?</h1>
</div>

<div class="flex gap-4 justify-center">
  <div v-click v-motion
    :initial="{ scale: 0 }"
    :enter="{ scale: 1 }"
    class="bg-white text-blue-600 px-8 py-4 rounded-full font-bold text-lg shadow-lg hover:shadow-xl transition-shadow cursor-pointer">
    <div class="flex items-center gap-2">
      <span>🎬</span>
      <span>Try Demo</span>
    </div>
  </div>

  <div v-click="2" v-motion
    :initial="{ scale: 0 }"
    :enter="{ scale: 1 }"
    class="bg-blue-800 text-white px-8 py-4 rounded-full font-bold text-lg shadow-lg hover:shadow-xl transition-shadow cursor-pointer">
    <div class="flex items-center gap-2">
      <span>💻</span>
      <span>View on GitHub</span>
    </div>
  </div>
</div>

<div v-click="3" class="mt-12 text-center">
  <p class="text-xl text-white opacity-90">Built with ❤️ at Reality Hackathon</p>
  <p class="mt-2 text-white opacity-75">Transform your ideas today!</p>
</div>

<style>
.slidev-layout {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}
</style>