<template>
  <div id="article-list">
    <!-- 面包屑导航 -->
    <div class="page">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>文章列表</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 文章列表 -->
    <div class="page" style="margin-top:10px">
      <el-row>
        <el-col v-for="item in article_list" :key="item.id" :span="24">
          <div class="card page">
            <el-row>
              <el-col :xs="24" :lg="6">
                <el-image
                  v-if="screenWidth > 500"
                  style="height:100px"
                  :src="item.cover"
                  :fit="'cover'"
                >
                </el-image>
                <el-image
                  v-else
                  style="width:100%"
                  :src="item.cover"
                  :fit="'cover'"
                ></el-image>
              </el-col>
              <el-col class="text-item" :xs="24" :lg="4">
                <span>{{ item.title }}</span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <span>发布者:{{ item.nickName }}</span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <el-button
                  @click="toArticle(item.id)"
                  type="success"
                  icon="el-icon-search"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  @click="deleteArticle(item.id)"
                ></el-button>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
    </div>
    <!-- 分页器 -->
    <div class="page" style="margin-top:10px">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        @current-change="currentChange"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import Qs from "qs"
export default {
  props: ["screenWidth"],
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      total: 100,
      article_list: []
    }
  },
  mounted() {
    this.getListData(this.currentPage)
  },
  methods: {
    // 提示框
    messageNotify(title, message, type) {
      this.$notify({
        title: title,
        message: message,
        type: type,
        showClose: true,
        center: true
      })
    },
    // 跳转至内容页
    toArticle(id) {
      this.$router.push({ path: "/article", query: { id: id } })
    },
    getListData(page) {
      axios({
        url: "http://127.0.0.1:9000/api/article-list/",
        method: "get",
        params: {
          page,
          pageSize: this.pageSize,
          category: "all"
        }
      }).then(res => {
        console.log(res.data)
        this.article_list = res.data.data
        this.total = res.data.total
      })
    },
    currentChange(val) {
      console.log("第" + val + "页")
      this.currentPage = val
      this.getListData(val)
    },
    // 删除文章
    deleteArticle(id) {
      if (confirm("是否确定删除")) {
        let checkInfo = {
          contentType: "auth_user",
          permissions: ["delete"]
        }
        this.$store.dispatch("checkUserPerm", checkInfo).then(res => {
          console.log(res)
          if (res) {
            axios({
              url: "http://127.0.0.1:9000/api/delete-article/",
              method: "delete",
              data: Qs.stringify({
                id,
                token: this.$store.getters.isnotUserLogin
              }),
              headers: {
                "Content-Type": "application/x-www-form-urlencoded"
              }
            }).then(res => {
              console.log(res)
              if (res.data == "nologin") {
                this.messageNotify("警告", "用户登录信息错误!", "error")
                return
              }
              if (res.data == "noperm") {
                this.messageNotify("警告", "权限不足!", "warning")
                return
              }
              this.getListData(this.currentPage, this.currentPage)
            })
          }
        })
      }
    }
  }
}
</script>

<style scoped>
#article-list .page {
  padding: 20px 10px;
}

.card.page .text-item {
  color: #fff;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
