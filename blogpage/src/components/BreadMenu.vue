<template>
  <div>
    <!-- 面包屑导航 -->
    <div class="page">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="category">{{ category }}</el-breadcrumb-item>
        <el-breadcrumb-item>{{ page_name }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
  </div>
</template>

<script>
export default {
  props: ['page_name', 'category'],
  data () {
    return {

    }
  },

}
</script>

<style scoped>
.page {
  padding: 10px 10px;
}
</style>