<template>
  <div id="add-article">
    <el-row :gutter="10">
      <el-col :xs="24" :lg="8">
        <div class="page">
          <el-form
            :label-position="'left'"
            label-width="80px"
            :model="article_info"
          >
            <el-form-item label="文章标题">
              <el-input v-model="article_info.title"></el-input>
            </el-form-item>
            <el-form-item label="描述">
              <el-input
                type="textarea"
                rows="4"
                v-model="article_info.describe"
              ></el-input>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
      <el-col :xs="24" :lg="16">
        <div class="page">
          <div v-for="(img, index) in cover_list" :key="index">
            <el-image
              v-if="img == cover_img"
              class="cover"
              style="width: 200px; height: 150px"
              :src="img"
              :fit="'cover'"
              @click="chooseCover(img)"
            ></el-image>
            <el-image
              v-else
              class=""
              style="width: 200px; height: 150px"
              :src="img"
              :fit="'cover'"
              @click="chooseCover(img)"
            ></el-image>
          </div>
          <el-button @click="submitArticle" type="success" round
            >保存文章</el-button
          >
        </div>
      </el-col>
      <el-col :xs="24" :lg="24">
        <div class="page">
          <div id="summernote"></div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import $ from "jquery"
import axios from "axios"
import Qs from "qs"
export default {
  data() {
    return {
      article_info: {
        title: "",
        describe: "",
        contents: ""
      },
      cover_img: "",
      cover_list: []
    }
  },
  mounted() {
    this.summernote()
  },
  methods: {
    //提示框
    messageNotify(title, message, type) {
      this.$notify({
        title: title,
        message: message,
        type: type,
        showClose: true,
        center: true
      })
    },
    //提交文章
    submitArticle() {
      let article_data = {
        title: this.article_info.title,
        describe: this.article_info.describe,
        content: this.article_info.contents,
        cover: this.cover_img,
        token: this.$store.getters.isnotUserLogin
      }
      axios
        .post(
          "http://127.0.0.1:9000/api/add-article/",
          Qs.stringify(article_data)
        )
        .then(res => {
          console.log(res)
          if (res.data == "no title") {
            this.messageNotify("警告", "文章标题不可为空!", "warning")
            return
          }
          if (res.data == "not login") {
            this.messageNotify("警告", "用户信息错误!", "warning")
            return
          }
          if (res.data == "ok") {
            window.location.reload()
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    summernote() {
      let self = this
      $("#summernote").summernote({
        width: "100%",
        height: 500,
        lang: "zh-CN",
        callbacks: {
          onChange(contents) {
            // console.log(contents)
            self.article_info.contents = contents
          },
          // 本地图片上传
          onImageUpload(files) {
            // console.log(files)
            let img = files[0]
            let imgData = new FileReader()
            imgData.readAsDataURL(img)
            // console.log(imgData)
            imgData.onload = function() {
              //   console.log(imgData.result)
              // 插入图片本身
              let imgnode = document.createElement("img")
              imgnode.src = imgData.result
              $("#summernote").summernote("insertNode", imgnode)
              // 推入封面选择
              self.cover_list.push(imgData.result)
            }
          },
          // 远程图片上传
          onImageLinkInsert(url) {
            console.log(url)
            let imgnode = document.createElement("img")
            imgnode.src = url
            console.log(imgnode)
            $("#summernote").summernote("insertNode", imgnode)
            self.cover_list.push(url)
          },
          // 删除媒体文件
          onMediaDelete(target) {
            let imgData = target[0].src
            console.log(imgData)
            for (let i = 0; i < self.cover_list.length; i++) {
              if (self.cover_list[i] == imgData) {
                self.cover_list.splice(i, 1)
              }
            }
          }
        }
      })
    },
    // 选择封面
    chooseCover(img) {
      this.cover_img = img
    }
  }
}
</script>

<style scoped>
.page {
  min-height: 200px;
  padding: 20px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page .el-image:hover {
  border: 2px solid #fcc815;
}

.page .el-image.cover {
  border: 2px solid #fcc815;
}

.el-form-item {
  margin-top: 22px;
}

.page .el-button {
  position: fixed;
  right: 20px;
  margin-top: 280px;
  z-index: 1001;
}
</style>
