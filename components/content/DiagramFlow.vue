<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'

const props = defineProps({
  nodes: {
    type: [Array, String],
    default: () => []
  },
  edges: {
    type: [Array, String],
    default: () => []
  },
  caption: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '500px'
  },
  showMinimap: {
    type: Boolean,
    default: false
  },
  showControls: {
    type: Boolean,
    default: true
  },
  background: {
    type: String,
    default: 'dots' // 'dots', 'lines', 'cross', 'none'
  },
  interactive: {
    type: Boolean,
    default: true
  },
  fitView: {
    type: Boolean,
    default: true
  },
  frame: {
    type: String,
    default: 'macos' // 'macos', 'browser', 'none'
  }
})

const isFullscreen = ref(false)
const vueFlowRef = ref(null)

// Parse nodes and edges if they come as strings
const parsedNodes = computed(() => {
  if (typeof props.nodes === 'string') {
    try {
      // Try to parse as JSON first
      return JSON.parse(props.nodes)
    } catch (e) {
      // If JSON parse fails, try to evaluate as JavaScript literal
      try {
        // Use Function constructor to safely evaluate JavaScript object literal
        const result = new Function('return ' + props.nodes)()
        return result
      } catch (e2) {
        console.error('Failed to parse nodes:', e2)
        return []
      }
    }
  }
  return props.nodes
})

const parsedEdges = computed(() => {
  if (typeof props.edges === 'string') {
    try {
      // Try to parse as JSON first
      return JSON.parse(props.edges)
    } catch (e) {
      // If JSON parse fails, try to evaluate as JavaScript literal
      try {
        // Use Function constructor to safely evaluate JavaScript object literal
        const result = new Function('return ' + props.edges)()
        return result
      } catch (e2) {
        console.error('Failed to parse edges:', e2)
        return []
      }
    }
  }
  return props.edges
})

// Initialize nodes and edges
const elements = computed(() => ({
  nodes: parsedNodes.value.map(node => {
    return {
      id: node.id,
      type: node.type || 'default',
      position: node.position || { x: 0, y: 0 },
      data: { 
        label: node.data?.label || node.label || node.id,
        style: node.style || {}
      },
      style: node.style || {},
      class: node.class || ''
    }
  }),
  edges: parsedEdges.value.map(edge => ({
    id: edge.id || `${edge.source}-${edge.target}`,
    source: edge.source,
    target: edge.target,
    type: edge.type || 'default',
    label: edge.label || '',
    animated: edge.animated || false,
    style: edge.style || {},
    markerEnd: edge.markerEnd || 'arrow'
  }))
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
    
    const container = vueFlowRef.value?.$el || vueFlowRef.value
    if (!container) return
    
    // Briefly hide UI controls before taking snapshot
    const controls = container.parentElement.querySelectorAll('.diagram-controls')
    controls.forEach(c => c.style.opacity = '0')
    
    const dataUrl = await toPng(container.parentElement, {
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

// Fit view on mount
onMounted(() => {
  if (props.fitView) {
    setTimeout(() => {
      try {
        const vueFlowInstance = vueFlowRef.value
        if (vueFlowInstance && vueFlowInstance.fitView) {
          vueFlowInstance.fitView({ padding: 0.2, duration: 200 })
        }
      } catch (err) {
        console.warn('Failed to fit view:', err)
      }
    }, 300)
  }
})

// Watch for nodes changes and refit
watch(() => parsedNodes.value, () => {
  if (props.fitView) {
    setTimeout(() => {
      try {
        const vueFlowInstance = vueFlowRef.value
        if (vueFlowInstance && vueFlowInstance.fitView) {
          vueFlowInstance.fitView({ padding: 0.2, duration: 200 })
        }
      } catch (err) {
        console.warn('Failed to fit view:', err)
      }
    }, 100)
  }
}, { deep: true })
</script>

<template>
  <ClientOnly>
    <figure 
      class="my-8 flex flex-col gap-3 group/wrapper" 
      :class="{ 'fixed inset-0 z-[9999] m-0 bg-white/80 dark:bg-black/80 backdrop-blur-sm flex items-center justify-center': isFullscreen }"
    >
    <div 
      class="relative w-full overflow-hidden border border-gray-200 dark:border-white/5 flex flex-col not-prose transition-all duration-300 shadow-sm"
      :class="[
        isFullscreen ? 'w-screen h-screen rounded-none shadow-2xl' : 'w-full rounded-2xl',
        'bg-gray-50 dark:bg-[#111113]'
      ]"
    >
      <!-- Frame Headers -->
      <div v-if="frame === 'macos' || frame === 'browser'" class="bg-[#dee1e6] dark:bg-[#2d2e32] flex flex-col gap-0 select-none border-b border-gray-200/50 dark:border-white/5 z-20">
        <div class="flex items-center px-4 h-10 relative">
          <div class="flex gap-2 items-center z-10">
            <div class="w-3 h-3 rounded-full bg-[#ff5f56] border-[0.5px] border-black/10"></div>
            <div class="w-3 h-3 rounded-full bg-[#ffbd2e] border-[0.5px] border-black/10"></div>
            <div class="w-3 h-3 rounded-full bg-[#27c93f] border-[0.5px] border-black/10"></div>
          </div>
          <div v-if="frame === 'browser'" class="absolute inset-x-0 top-1/2 -translate-y-1/2 flex justify-center pointer-events-none">
            <div class="bg-white/60 dark:bg-[#1e1e1e]/60 rounded-md px-3 py-1.5 text-[11px] text-gray-500 flex items-center justify-center gap-2 w-full max-w-[240px] shadow-sm">
              <svg class="w-3 h-3 opacity-50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              localhost:3000
            </div>
          </div>
        </div>
      </div>

      <!-- Vue Flow Container -->
      <div 
        class="relative flex-grow"
        :style="{ height: isFullscreen ? '100%' : height }"
      >
        <VueFlow
          ref="vueFlowRef"
          :nodes="elements.nodes"
          :edges="elements.edges"
          :fit-view-on-init="fitView"
          :nodes-draggable="interactive"
          :nodes-connectable="false"
          :elements-selectable="interactive"
          :zoom-on-scroll="interactive"
          :pan-on-scroll="false"
          :pan-on-drag="interactive"
          class="vue-flow-custom"
        >
          <Background 
            v-if="background !== 'none'"
            :pattern-color="'var(--vf-background-pattern)'"
            :variant="background"
            :gap="16"
          />
          <Controls v-if="showControls" />
          <MiniMap v-if="showMinimap" />
        </VueFlow>
      </div>

      <!-- Toolbar Overlay -->
      <div class="absolute top-2 right-2 flex gap-1 z-30 opacity-0 group-hover/wrapper:opacity-100 transition-opacity duration-200 diagram-controls" :class="{ 'opacity-100': isFullscreen }">
        <button 
          @click="toggleFullscreen" 
          class="p-1.5 bg-white/80 dark:bg-black/50 hover:bg-white dark:hover:bg-black backdrop-blur rounded-md text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white border border-gray-200 dark:border-white/10 transition-colors shadow-sm" 
          title="Toggle Fullscreen"
        >
          <svg v-if="!isFullscreen" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" /></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
        <button 
          @click="downloadImage" 
          class="p-1.5 bg-white/80 dark:bg-black/50 hover:bg-white dark:hover:bg-black backdrop-blur rounded-md text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white border border-gray-200 dark:border-white/10 transition-colors shadow-sm" 
          title="Download Image"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
        </button>
      </div>
    </div>

    <!-- Caption -->
    <figcaption v-if="caption && !isFullscreen" class="text-center text-[13px] text-gray-500 dark:text-gray-400 font-medium">
      {{ caption }}
    </figcaption>
  </figure>
  
  <template #fallback>
    <div class="my-8 flex items-center justify-center h-[500px] bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-white/5">
      <div class="text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
        <p class="text-sm text-gray-500 dark:text-gray-400">Завантаження діаграми...</p>
      </div>
    </div>
  </template>
  </ClientOnly>
</template>

<style>
/* Vue Flow Custom Styling */
.vue-flow-custom {
  --vf-node-bg: #ffffff;
  --vf-node-text: #1a1a1a;
  --vf-node-border: #e5e7eb;
  --vf-connection-path: #3b82f6;
  --vf-handle: #3b82f6;
  --vf-background-pattern: #d1d5db;
}

.dark .vue-flow-custom {
  --vf-node-bg: #1e1e1e;
  --vf-node-text: #e5e5e5;
  --vf-node-border: #404040;
  --vf-connection-path: #60a5fa;
  --vf-handle: #60a5fa;
  --vf-background-pattern: #404040;
}

/* Custom node styling */
.vue-flow-custom .vue-flow__node {
  background: var(--vf-node-bg);
  border: 2px solid var(--vf-node-border);
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--vf-node-text);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.vue-flow-custom .vue-flow__node:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.vue-flow-custom .vue-flow__node.selected {
  border-color: var(--vf-connection-path);
  box-shadow: 0 0 0 2px var(--vf-connection-path);
}

/* Edge styling */
.vue-flow-custom .vue-flow__edge-path {
  stroke: var(--vf-connection-path);
  stroke-width: 2;
}

.vue-flow-custom .vue-flow__edge.animated .vue-flow__edge-path {
  stroke-dasharray: 5;
  animation: dashdraw 0.5s linear infinite;
}

.vue-flow-custom .vue-flow__edge-text {
  font-size: 12px;
  fill: var(--vf-node-text);
}

.vue-flow-custom .vue-flow__edge-textbg {
  fill: var(--vf-node-bg);
}

.vue-flow-custom .vue-flow__edge .vue-flow__edge-textwrapper {
  pointer-events: all;
}

/* Handle styling */
.vue-flow-custom .vue-flow__handle {
  width: 8px;
  height: 8px;
  background: var(--vf-handle);
  border: 2px solid #fff;
}

/* Controls styling */
.vue-flow-custom .vue-flow__controls {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.vue-flow-custom .vue-flow__controls-button {
  background: var(--vf-node-bg);
  border-bottom: 1px solid var(--vf-node-border);
  color: var(--vf-node-text);
}

.vue-flow-custom .vue-flow__controls-button:hover {
  background: var(--vf-node-border);
}

/* Minimap styling */
.vue-flow-custom .vue-flow__minimap {
  background: var(--vf-node-bg);
  border: 1px solid var(--vf-node-border);
  border-radius: 8px;
}

@keyframes dashdraw {
  from {
    stroke-dashoffset: 10;
  }
}
</style>
