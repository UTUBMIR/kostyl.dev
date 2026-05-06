<template>
  <figure class="my-8 flex flex-col gap-3 group/wrapper" :class="{ 'fixed inset-0 z-[9999] m-0 bg-white/80 dark:bg-black/80 backdrop-blur-sm flex items-center justify-center': isFullscreen }">
    <!-- The Canvas Container -->
    <div 
      ref="canvasRef"
      class="relative w-full overflow-hidden border border-gray-200 dark:border-white/5 flex flex-col not-prose transition-all duration-300 shadow-sm"
      :class="[
        isFullscreen ? 'w-screen h-screen rounded-none shadow-2xl scale-100 overflow-y-auto' : 'w-full rounded-2xl',
        bgClass
      ]"
      :style="cssVars"
    >
      <!-- Frame Headers -->
      <div v-if="frame === 'macos' || frame === 'browser'" class="bg-[#dee1e6] dark:bg-[#2d2e32] flex flex-col gap-0 select-none border-b border-gray-200/50 dark:border-white/5 z-20">
        <!-- macOS Buttons Row -->
        <div class="flex items-center px-4 h-10 relative">
          <div class="flex gap-2 items-center z-10">
            <div class="w-3 h-3 rounded-full bg-[#ff5f56] border-[0.5px] border-black/10"></div>
            <div class="w-3 h-3 rounded-full bg-[#ffbd2e] border-[0.5px] border-black/10"></div>
            <div class="w-3 h-3 rounded-full bg-[#27c93f] border-[0.5px] border-black/10"></div>
          </div>
          <!-- Title / Address Bar -->
          <div v-if="frame === 'browser'" class="absolute inset-x-0 top-1/2 -translate-y-1/2 flex justify-center pointer-events-none">
             <div class="bg-white/60 dark:bg-[#1e1e1e]/60 rounded-md px-3 py-1.5 text-[11px] text-gray-500 flex items-center justify-center gap-2 w-full max-w-[240px] shadow-sm">
               <svg class="w-3 h-3 opacity-50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
               localhost:3000
             </div>
          </div>
        </div>
      </div>
      <div v-else-if="frame === 'terminal'" class="bg-gray-900 flex items-center px-4 h-10 select-none border-b border-white/10 z-20">
         <div class="flex gap-2 items-center">
            <div class="w-3 h-3 rounded-full bg-[#ff5f56]"></div>
            <div class="w-3 h-3 rounded-full bg-[#ffbd2e]"></div>
            <div class="w-3 h-3 rounded-full bg-[#27c93f]"></div>
          </div>
          <div class="mx-auto text-gray-400 text-xs font-mono">bash — 80x24</div>
      </div>

      <!-- Canvas Area (where content goes) -->
      <div class="relative flex-grow flex items-center justify-center overflow-hidden" :class="[paddingClass, minHeightClass]">
        
        <!-- Grid Pattern -->
        <svg v-if="pattern === 'grid'" class="absolute inset-0 w-full h-full pointer-events-none opacity-[0.04] dark:opacity-[0.05] text-black dark:text-white" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern :id="gridId" width="24" height="24" patternUnits="userSpaceOnUse">
              <path d="M 24 0 L 0 0 0 24" fill="none" stroke="currentColor" stroke-width="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" :fill="`url(#${gridId})`" />
        </svg>
        
        <!-- Dots Pattern -->
        <svg v-else-if="pattern === 'dots'" class="absolute inset-0 w-full h-full pointer-events-none opacity-[0.1] dark:opacity-[0.15] text-black dark:text-white" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern :id="dotsId" width="20" height="20" patternUnits="userSpaceOnUse">
              <circle cx="2" cy="2" r="1.5" fill="currentColor"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" :fill="`url(#${dotsId})`" />
        </svg>

        <!-- Gradient Fade for visual depth -->
        <div v-if="pattern !== 'none'" class="absolute inset-0 bg-gradient-to-t from-transparent to-white/30 dark:to-black/30 pointer-events-none"></div>
        
        <!-- Content Slot -->
        <div 
          class="relative z-10 flex items-center justify-center w-full group/canvas block" 
          :data-step="currentStep"
        >
          <MDCSlot :use="$slots.default" unwrap="p" />
        </div>
      </div>
      
      <!-- Toolbar Overlay -->
      <div class="absolute top-2 right-2 flex gap-1 z-30 opacity-0 group-hover/wrapper:opacity-100 transition-opacity duration-200 canvas-controls" :class="{ 'opacity-100': isFullscreen }">
        <!-- Fullscreen Button -->
        <button @click="toggleFullscreen" class="p-1.5 bg-white/80 dark:bg-black/50 hover:bg-white dark:hover:bg-black backdrop-blur rounded-md text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white border border-gray-200 dark:border-white/10 transition-colors shadow-sm" title="Toggle Fullscreen">
          <svg v-if="!isFullscreen" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" /></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
        <!-- Download Button -->
        <button @click="downloadImage" class="p-1.5 bg-white/80 dark:bg-black/50 hover:bg-white dark:hover:bg-black backdrop-blur rounded-md text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white border border-gray-200 dark:border-white/10 transition-colors shadow-sm" title="Download Image">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
        </button>
      </div>

      <!-- Controls for Steps -->
      <div v-if="maxSteps > 1" class="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-3 px-4 py-1.5 bg-white/90 dark:bg-black/80 backdrop-blur-md rounded-full shadow-lg border border-gray-200 dark:border-white/10 z-30 canvas-controls">
        <button @click="prevStep" :disabled="currentStep === 1" class="text-gray-500 hover:text-gray-800 dark:hover:text-white disabled:opacity-30 disabled:hover:text-gray-500">
           <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </button>
        <span class="text-xs font-bold text-gray-600 dark:text-gray-300 min-w-[50px] text-center">{{ currentStep }} / {{ maxSteps }}</span>
        <button @click="nextStep" :disabled="currentStep === maxSteps" class="text-gray-500 hover:text-gray-800 dark:hover:text-white disabled:opacity-30 disabled:hover:text-gray-500">
           <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        </button>
      </div>
    </div>

    <!-- Optional Caption -->
    <figcaption v-if="caption && !isFullscreen" class="text-center text-[13px] text-gray-500 dark:text-gray-400 font-medium">
      {{ caption }}
    </figcaption>
  </figure>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  caption: { type: String, default: '' },
  pattern: { type: String, default: 'grid' }, // 'none', 'grid', 'dots'
  bg: { type: String, default: 'soft' }, // 'transparent', 'soft', 'dark', 'white'
  padding: { type: String, default: 'p-8 sm:p-12' },
  minHeight: { type: String, default: 'min-h-[250px]' },
  viewBox: { type: String, default: '0 0 1000 600' },
  steps: { type: [Number, String], default: 1 },
  frame: { type: String, default: 'none' } // 'none', 'macos', 'browser', 'terminal'
})

const currentStep = ref(1)
const isFullscreen = ref(false)
const canvasRef = ref(null)

const maxSteps = computed(() => Number(props.steps) || 1)

const nextStep = () => {
  if (currentStep.value < maxSteps.value) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

// Unique IDs for SVG patterns to avoid conflicts
const gridId = `grid-${Math.random().toString(36).substr(2, 9)}`
const dotsId = `dots-${Math.random().toString(36).substr(2, 9)}`

const bgClass = computed(() => {
  switch(props.bg) {
    case 'transparent': return 'bg-transparent'
    case 'dark': return 'bg-gray-900 dark:bg-[#0d0d0f]'
    case 'white': return 'bg-white dark:bg-[#1a1b1e]'
    case 'soft':
    default:
      return 'bg-gray-50 dark:bg-[#111113]'
  }
})

const paddingClass = computed(() => props.padding)
const minHeightClass = computed(() => props.minHeight)

// Provide some basic CSS variables for semantic usage
const cssVars = computed(() => ({
  '--canvas-primary': 'var(--color-primary-500, #3b82f6)',
  '--canvas-accent': 'var(--color-orange-500, #f97316)',
  '--canvas-muted': 'var(--color-gray-500, #6b7280)'
}))

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
  if (isFullscreen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

// Download functionality
const downloadImage = async () => {
  try {
    const { toPng } = await import('html-to-image')
    
    // Briefly hide UI controls before taking snapshot
    const controls = canvasRef.value.querySelectorAll('.canvas-controls')
    controls.forEach(c => c.style.opacity = '0')
    
    const dataUrl = await toPng(canvasRef.value, {
      quality: 1,
      pixelRatio: 2, // retina quality
      style: {
        transform: 'scale(1)',
      }
    })
    
    // Restore controls
    controls.forEach(c => c.style.opacity = '')
    
    const link = document.createElement('a')
    link.download = `diagram-${Math.random().toString(36).substr(2, 6)}.png`
    link.href = dataUrl
    link.click()
  } catch (err) {
    console.error('Failed to export image', err)
    alert('Не вдалося завантажити зображення.')
  }
}
</script>
