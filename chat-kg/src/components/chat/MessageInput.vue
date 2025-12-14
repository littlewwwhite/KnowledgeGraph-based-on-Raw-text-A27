<template>
  <div class="input-box">
    <a-button size="large" @click="$emit('clear')">
      <template #icon> <ClearOutlined /> </template>
    </a-button>
    <a-input
      type="text"
      class="user-input"
      v-model:value="inputValue"
      @keydown.enter="handleSend"
      placeholder="输入问题……"
    />
    <a-button size="large" @click="handleSend" :disabled="!inputValue">
      <template #icon> <SendOutlined /> </template>
    </a-button>
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
.input-box {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-top: 1px solid #ccc;
}

input.user-input {
  flex: 1;
  height: 40px;
  padding: 0.5rem 1rem;
  background-color: #fff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.1);
  font-size: 1.2rem;
  margin: 0 0.6rem;
  color: #111111;
  font-size: 16px;
  font-variation-settings: 'wght' 400, 'opsz' 10.5;
}

.ant-btn-icon-only {
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
}
</style>
