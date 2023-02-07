<template>
  <div>
    <!-- 面包屑导航 -->
    <BreadMenu :page_name="'栏目管理'"></BreadMenu>

    <!-- 内容 -->
    <div class="body page">
      <el-row :gutter="10">
        <el-col :span="6">
          <div class="page">
            <h5>栏目结构</h5>
            <el-divider></el-divider>
          </div>
          <div class="body page" style="display:flex">
            <el-input
              v-model="new_category_name"
              placeholder="请输入新栏目名称"
            ></el-input>
            <el-button @click="pushCategoryList()" type="success"
              >保存</el-button
            >
          </div>
          <div class="body page">
            <el-tree
              :data="category_tree"
              node-key="id"
              default-expand-all
              draggable
              :render-content="renderContent"
              @node-click="choosed_category_articleList"
            >
            </el-tree>
          </div>
          <div class="save-tree body page" style="float:left">
            <el-button @click="getCategoryTree()" type="warning" size="mini"
              >恢复结构</el-button
            >
            <el-button @click="saveCategoryTree()" type="success" size="mini"
              >保存结构</el-button
            >
            <el-button type="primary" size="mini">文章获取</el-button>
          </div>
        </el-col>

        <el-col :span="18">
          <div class="page">
            <h5>文章列表</h5>
            <el-divider></el-divider>
          </div>
          <!-- 文章列表 -->
          <div class="page" style="margin-top:10px;min-height:468px">
            <el-row>
              <el-col v-for="item in article_list" :key="item.id" :span="24">
                <div class="card page">
                  <el-row>
                    <el-col :xs="24" :lg="6">
                      <el-image
                        style="height:100px"
                        :src="item.cover"
                        :fit="'cover'"
                      >
                      </el-image>
                    </el-col>
                    <el-col class="text-item" :xs="24" :lg="4">
                      <span>{{ item.title }}</span>
                    </el-col>
                    <el-col class="text-item" :xs="12" :lg="7">
                      <span>发布者:{{ item.nickName }}</span>
                    </el-col>
                    <el-col class="text-item" :xs="12" :lg="7">
                      <el-popover placement="right" width="80" trigger="click">
                        <el-tree
                          :data="category_tree"
                          node-key="id"
                          default-expand-all
                          @node-click="choosed_category"
                        >
                        </el-tree>
                        <el-button
                          type="warning"
                          icon="el-icon-plus"
                          circle
                          slot="reference"
                        ></el-button>
                        <el-button
                          @click="saveArticleToCategory(item.id)"
                          type="success"
                          size="mini"
                          >确定</el-button
                        >
                      </el-popover>
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
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import BreadMenu from "../components/BreadMenu.vue"
import axios from "axios"
import Qs from "qs"
export default {
  data() {
    return {
      // 文章列表
      currentPage: 1,
      currentCategory: "nobelong",
      pageSize: 4,
      total: 100,
      article_list: [],
      // 栏目名称
      new_category_name: "",
      // 栏目结构
      maxId: 0,
      category_tree: [],
      // 文章栏目分配
      choosed_category_id: 0,
      choosed_article_id: 0
    }
  },
  components: {
    BreadMenu
  },
  mounted() {
    console.log(this.currentCategory)
    this.getListData(this.currentPage, this.currentCategory)
    this.getCategoryTree()
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
    // 选择栏目查看文章
    choosed_category_articleList(node) {
      let category_name = node.label
      this.getListData(1, category_name)
    },
    // 选择文章保存栏目
    choosed_category(node) {
      // console.log(node)
      this.choosed_category_id = node.id
      this.choosed_category_name = node.label
    },
    saveArticleToCategory(article_id) {
      axios({
        url: "http://127.0.0.1:9000/api/add-article/",
        method: "put",
        data: Qs.stringify({
          token: this.$store.getters.isnotUserLogin,
          category_id: this.choosed_category_id,
          article_id: article_id
        })
      }).then(res => {
        if (res.data == "nologin") {
          this.messageNotify("警告", "尚未登录!", "warning")
          return
        }
        if (res.data == "noperm") {
          this.messageNotify("警告", "权限不足!", "warning")
          return
        }
        if (res.data == "ok") {
          console.log(res.data)
          this.getListData(1, this.choosed_category_name)
          this.getCategoryTree()
        }
      })
    },
    // 获取栏目数据
    getCategoryTree() {
      axios({
        url: "http://127.0.0.1:9000/api/wong-category/",
        method: "get"
      }).then(res => {
        console.log(res.data)
        this.category_tree = res.data
      })
    },
    // 保存栏目结构
    saveCategoryTree() {
      console.log(this.category_tree)
      axios({
        url: "http://127.0.0.1:9000/api/wong-category/",
        method: "put",
        data: Qs.stringify({
          token: this.$store.getters.isnotUserLogin,
          category_tree: JSON.stringify(this.category_tree)
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
      })
    },
    // 新栏目名称
    pushCategoryList() {
      let checkTree = this.loopCheckData(this.category_tree)
      console.log(checkTree)
      if (checkTree == false) {
        this.new_category_name = ""
        return
      }
      let new_category = {
        id: this.maxId + 1,
        label: this.new_category_name,
        children: []
      }
      console.log(new_category)
      this.category_tree.push(new_category)
      this.new_category_name = ""
    },
    // 递归查询最大id
    loopCheckData(tree) {
      let checkTree = true
      // 检查原栏目数据
      tree.forEach(obj => {
        if (obj.id > this.maxId) {
          this.maxId = obj.id
        }
        if (obj.label == this.new_category_name) {
          this.messageNotify("警告", "栏目名重复!", "warning")
          checkTree = false
          return
        }
        if (obj.children) {
          if (obj.children.length > 0) {
            this.loopCheckData(obj.children)
          }
        }
      })
      return checkTree
    },
    getListData(page, category) {
      axios({
        url: "http://127.0.0.1:9000/api/article-list/",
        method: "get",
        params: {
          page,
          pageSize: this.pageSize,
          category: category
        }
      }).then(res => {
        // console.log(res.data)
        this.article_list = res.data.data
        this.total = res.data.total
      })
    },
    currentChange(val) {
      console.log("第" + val + "页")
      this.currentPage = val
      this.getListData(val, this.currentCategory)
    },
    remove(_, data) {
      console.log(data.id)
      axios({
        url: "http://127.0.0.1:9000/api/wong-category/",
        method: "delete",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        data: Qs.stringify({
          token: this.$store.getters.isnotUserLogin,
          id: data.id
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
          this.getCategoryTree()
        }
      })
    },
    renderContent(h, { node, data }) {
      return (
        <span class="custom-tree-node">
          <span>{node.label}</span>
          <span>({node.data.article_num})</span>
          <span>
            <el-button
              size="mini"
              type="text"
              style="margin-left:20px"
              on-click={() => this.remove(node, data)}
            >
              删除
            </el-button>
          </span>
        </span>
      )
    }
  }
}
</script>

<style scoped>
.page {
  padding: 10px 10px;
}

.card.page .text-item {
  color: #fff;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.text-item span {
  height: 40px;
  line-height: 20px;
  text-overflow: ellipsis;
  overflow: hidden;
}

.save-tree button {
  margin: 5px 5px;
}
</style>
