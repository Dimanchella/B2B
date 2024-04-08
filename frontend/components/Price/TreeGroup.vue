<script setup>
const emit = defineEmits(["groupClick"])
const props = defineProps({
  group: {
    type: Object
  },
  groupTitle: {
    type: String
  },
  groupChildren: {
    type: Array,
    default: []
  },
  depth: {
    type: Number,
    default: 0
  }
})

const expanded = ref(false)

const expand = () => {
  expanded.value = !expanded.value
}

const groupClickParent = (group) => {
  //alert("TreeGroup.groupClickParent: " + group.title);
  emit("groupClick", group)
}

const groupClickChild = (group) => {
  //alert("TreeGroup.groupClickChild: " + group.title);
  emit("groupClick", group)
}

const hasChildren = computed(() => {
  return props.group.children.length > 0
})
</script>

<template>
  <div>
    <div
        :style="{'margin-left': `${depth}px`}"
        class="node"
    >
      <span
          v-if="hasChildren"
          @click="expand"
      >
        {{ expanded ? '&#9660; ' : '&#9658; ' }}
      </span>
      <span
          v-else
      >• </span>
      <span
          @click="groupClickParent(group)"
      >
        {{ groupTitle }}
      </span>
    </div>
    <PriceTreeGroup
        v-if="expanded"
        v-for="chGroup in groupChildren"
        :key="chGroup.id"
        :group="chGroup"
        :group-title="chGroup.title"
        :group-children="chGroup.children"
        :depth="depth + 10"
        @groupClick="groupClickParent"
    />
  </div>
</template>

<style scoped>

.node {
font-size:1.2em; 
line-height:1.85rem; 
cursor:pointer;
}

</style>
