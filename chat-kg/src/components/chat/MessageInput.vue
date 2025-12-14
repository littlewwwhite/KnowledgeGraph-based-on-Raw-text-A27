<template>
  <div class="input-area">
    <div class="input-container">
      <button
        class="action-btn clear-btn"
        @click="$emit('clear')"
        title="Clear chat"
      >
        <ClearOutlined />
      </button>

      <div class="input-wrapper">
        <input
          type="text"
          class="message-input"
          v-model="inputValue"
          @keydown.enter="handleSend"
          placeholder="Ask a question..."
        />
      </div>

      <button
        class="action-btn send-btn"
        :class="{ active: inputValue.trim() }"
        @click="handleSend"
        :disabled="!inputValue.trim()"
        title="Send message"
      >
        <SendOutlined />
      </button>
    </div>
    <p class="input-hint">Press Enter to send</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { SendOutlined, ClearOutlined } from '@ant-design/icons-vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'send', 'clear'])

const inputValue = ref(props.modelValue)

watch(
  () => props.modelValue,
  (newVal) => {
    inputValue.value = newVal
  }
)

watch(inputValue, (newVal) => {
  emit('update:modelValue', newVal)
})

const handleSend = () => {
  if (inputValue.value.trim()) {
    emit('send', inputValue.value)
  }
}
</script>

<style lang="less" scoped>
.input-area {
  padding: var(--space-4) var(--space-6);
  background: var(--color-neutral-0);
  border-top: 1px solid var(--color-neutral-150);
}

.input-container {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.input-wrapper {
  flex: 1;
  position: relative;
}

.message-input {
  width: 100%;
  height: 48px;
  padding: var(--space-3) var(--space-4);
  background: var(--color-neutral-100);
  border: 2px solid transparent;
  border-radius: var(--radius-xl);
  font-size: var(--text-base);
  font-family: var(--font-sans);
  color: var(--color-neutral-800);
  transition: all var(--duration-fast) var(--ease-default);

  &::placeholder {
    color: var(--color-neutral-400);
  }

  &:hover {
    background: var(--color-neutral-150);
  }

  &:focus {
    outline: none;
    background: var(--color-neutral-0);
    border-color: var(--color-primary-500);
    box-shadow: 0 0 0 4px rgba(60, 165, 191, 0.12);
  }
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border: none;
  border-radius: var(--radius-lg);
  font-size: var(--text-lg);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-default);

  &:disabled {
    cursor: not-allowed;
    opacity: 0.4;
  }
}

.clear-btn {
  background: var(--color-neutral-100);
  color: var(--color-neutral-500);

  &:hover:not(:disabled) {
    background: var(--color-neutral-200);
    color: var(--color-neutral-700);
  }

  &:active:not(:disabled) {
    transform: scale(0.95);
  }
}

.send-btn {
  background: var(--color-neutral-200);
  color: var(--color-neutral-400);

  &.active {
    background: var(--msg-sent-bg);
    color: var(--color-neutral-0);
    box-shadow: var(--shadow-primary);

    &:hover:not(:disabled) {
      filter: brightness(1.05);
      box-shadow: 0 6px 20px rgba(60, 165, 191, 0.35);
    }

    &:active:not(:disabled) {
      transform: scale(0.95);
    }
  }
}

.input-hint {
  margin: var(--space-2) 0 0 0;
  font-size: var(--text-xs);
  color: var(--color-neutral-400);
  text-align: center;
  opacity: 0;
  transition: opacity var(--duration-fast) var(--ease-default);
}

.input-area:focus-within .input-hint {
  opacity: 1;
}

@media (max-width: 768px) {
  .input-area {
    padding: var(--space-3) var(--space-4);
  }

  .message-input {
    height: 44px;
  }

  .action-btn {
    width: 40px;
    height: 40px;
  }

  .input-hint {
    display: none;
  }
}
</style>
