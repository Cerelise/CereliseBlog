<template>
  <!-- 面包屑导航 -->
  <div class="dweb">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item v-if="lanmu">{{ lanmu | capitalize }}</el-breadcrumb-item>
      <el-breadcrumb-item>{{ page_name }}</el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>

<script>
export default {
  props: ['page_name', 'lanmu'],
  data() {
    return {};
  },
  components: {},
  filters: {
    capitalize: function(value) {
      if (value == 'nobelong') {
        return '未知栏目';
      }
      return value;
    },
  },
};
</script>
<style scoped>
.dweb {
  padding: 20px 10px;
}
</style>
