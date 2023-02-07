<template>
  <div>
    <!-- 面包屑导航 -->
    <BreadMenu
      :page_name="article_data.title"
      :category="article_data.category"
    ></BreadMenu>

    <!-- 文章内容 -->
    <el-row :gutter="10">
      <el-col :xs="24" :lg="16">
        <div class="body page">
          <div class="header">
            {{ article_data.title }}
          </div>
        </div>
        <div class="body page">
          <div class="page">
            {{ article_data.describe }}
          </div>
        </div>

        <div class="body page">
          <div class="article-content" v-html="article_data.content">
            <!-- 文章内容 -->
          </div>
          <div class="clear"></div>
        </div>

        <div class="body page">
          <el-button
            v-if="article_data.pre_id == 0"
            @click="toOtherPage(article_data.pre_id)"
            type="info"
            >上一页</el-button
          >
          <el-button
            v-else
            @click="toOtherPage(article_data.pre_id)"
            type="success"
            >上一页</el-button
          >
          <el-button
            v-if="article_data.next_id == 0"
            @click="toOtherPage(article_data.next_id)"
            type="info"
            >下一页</el-button
          >
          <el-button
            v-else
            @click="toOtherPage(article_data.next_id)"
            type="success"
            >下一页</el-button
          >
        </div>
      </el-col>

      <el-col :xs="24" :lg="8">
        <div class="body page">
          <el-image :src="article_data.cover" :fit="'cover'"></el-image>
        </div>
        <!-- 白嫖区域 -->
        <div class="body page like-btn">
          <el-row>
            <el-col :span="12">
              <i
                v-if="user_article_info.like"
                class="iconfont icon-dianzan"
                style="color:#ff5959"
                @click="toLike()"
              ></i>
              <i @click="toLike()" v-else class="iconfont icon-dianzan"></i>
            </el-col>
            <el-col :span="12">
              <i
                v-if="user_article_info.favor"
                class="iconfont icon-shoucang"
                style="color:#ffc815"
                @click="toFavor()"
              ></i>
              <i @click="toFavor()" v-else class="iconfont icon-shoucang"></i>
            </el-col>
          </el-row>
        </div>

        <!-- 评论区 -->
        <div class="body page">
          <div
            v-for="(item, index) in comment_data"
            :key="index"
            class="body page comment-item"
          >
            {{ item.nickName }}说：
            <el-divider></el-divider>
            {{ item.text }}
          </div>
        </div>
        <!-- 分页器 -->
        <div class="page" style="margin-top:10px">
          <el-pagination
            background
            small
            :pager-count="5"
            layout="prev, pager, next"
            :total="comment_total"
            :page-size="comment_pageSize"
            @current-change="commentCurrentChange"
          >
          </el-pagination>
        </div>
        <!-- 新评论 -->
        <div class="body page">
          <el-input
            type="textarea"
            :maxlength="100"
            :rows="2"
            placeholder="请输入内容"
            v-model="new_comment"
          >
          </el-input>
          <el-button @click="saveNewComment()" type="success"
            >发表评论</el-button
          >
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios"
import Qs from "qs"
import BreadMenu from "../components/BreadMenu.vue"
export default {
  data() {
    return {
      article_id: this.$route.query.id,
      article_data: {},
      user_article_info: {},
      // 评论
      new_comment: "",
      comment_total: 100,
      comment_pageSize: 4,
      comment_data: []
    }
  },
  components: {
    BreadMenu
  },
  watch: {
    $route(to) {
      // console.log(to)
      this.article_id = to.query.id
      this.getArticleData(to.query.id)
      this.getUserArticleInfo()
      this.getAllComments(1, this.comment_pageSize)
    }
  },
  mounted() {
    this.getArticleData(this.article_id)
    this.getAllComments(1, this.comment_pageSize)
    this.getUserArticleInfo()
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
    // 点赞
    toLike() {
      axios({
        url: "http://127.0.0.1:9000/api/article-like/",
        method: "post",
        data: Qs.stringify({
          token: this.$store.getters.isnotUserLogin,
          article_id: this.article_id
        })
      }).then(res => {
        console.log(res.data)
        if (res.data == "nologin") {
          this.messageNotify("警告", "尚未登录!", "warning")
          return
        }
        if (res.data == "ok") {
          this.getUserArticleInfo()
        }
      })
    },
    // 收藏
    toFavor() {
      axios({
        url: "http://127.0.0.1:9000/api/article-favor/",
        method: "post",
        data: Qs.stringify({
          token: this.$store.getters.isnotUserLogin,
          article_id: this.article_id
        })
      }).then(res => {
        console.log(res.data)
        if (res.data == "nologin") {
          this.messageNotify("警告", "尚未登录!", "warning")
          return
        }
        if (res.data == "ok") {
          this.getUserArticleInfo()
        }
      })
    },
    // 获取用户活动信息
    getUserArticleInfo() {
      let token = this.$store.getters.isnotUserLogin
      if (token) {
        axios({
          url: "http://127.0.0.1:9000/api/user-article-info/",
          method: "post",
          data: Qs.stringify({
            token: token,
            article_id: this.article_id
          })
        }).then(res => {
          console.log(res.data)
          this.user_article_info = res.data
        })
      }
    },
    // 获取文章评论
    getAllComments(page, pageSize) {
      axios({
        url: "http://127.0.0.1:9000/api/wong-comment/",
        method: "get",
        params: {
          page,
          pageSize,
          article_id: this.article_id
        }
      }).then(res => {
        // console.log(res.data)
        this.comment_data = res.data.data
        this.comment_total = res.data.total
      })
    },
    // 发表评论
    saveNewComment() {
      if (this.new_comment.length == 0) {
        this.messageNotify("警告", "评论内容为空!", "warning")
        return
      }
      axios({
        url: "http://127.0.0.1:9000/api/wong-comment/",
        method: "post",
        data: Qs.stringify({
          token: this.$store.getters.isnotUserLogin,
          article_id: this.article_id,
          text: this.new_comment
        })
      }).then(res => {
        console.log(res.data)
        if (res.data == "nologin") {
          this.messageNotify("警告", "尚未登录!", "warning")
          return
        }
        if (res.data == "noperm") {
          this.messageNotify("警告", "权限不足!", "warning")
          return
        }
        if (res.data == "ok") {
          this.getAllComments(1, this.comment_pageSize)
        }
      })
    },
    // 评论翻页
    commentCurrentChange(page) {
      this.getAllComment(page, this.comment_pageSize)
    },
    // 跳转文章页
    toOtherPage(id) {
      if (id == 0) {
        this.messageNotify("警告", "没有了!", "warning")
        return
      }
      this.$router.push({ path: "/article", query: { id: id } })
    },
    getArticleData(id) {
      // console.log(id)
      axios({
        url: "http://127.0.0.1:9000/api/view-article/",
        method: "get",
        params: {
          article_id: id
        }
      }).then(res => {
        //  console.log(res.data)
        this.article_data = res.data
      })
    }
  }
}
</script>

<style scoped>
.body.page .page {
  padding: 10px;
  color: #b7b7b7;
  font-size: 12px;
  font-style: italic;
}

.body.page {
  padding: 10px 10px;
}

.article-content {
  color: #fff;
}

.like-btn {
  text-align: center;
  color: #fff;
}
.like-btn i {
  font-size: 30px;
  cursor: pointer;
}
.body.page.comment-item {
  color: #fff;
  font-size: 18px;
  font-style: normal;
}
</style>
