<template>
  <div>
    <!-- 面包屑导航 -->
    <div class="page">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="body page">
      <div class="page">
        <h5>新建用户组</h5>
        <el-divider></el-divider>
      </div>

      <el-row :gutter="10">
        <el-col :xs="24" :lg="12">
          <div class="new-group page">
            <el-form :inline="true" :model="new_group" class="demo-form-inline">
              <el-form-item>
                <el-input
                  v-model="new_group.name"
                  placeholder="新用户组名称"
                ></el-input>
              </el-form-item>

              <el-form-item>
                <el-button @click="saveNewGroup()" type="primary"
                  >保存</el-button
                >
              </el-form-item>
            </el-form>
          </div>
        </el-col>

        <el-col :xs="24" :lg="12">
          <div class="perm-list page">
            <el-row>
              <el-col
                v-for="(item, index) in new_group.checkList"
                :key="index"
                :span="24"
                style="border-bottom:1px solid #fff;padding:5px 0"
              >
                <el-button
                  @click="chooseAllmethod(index)"
                  type="primary"
                  plain
                  style="float:left;margin-right:10px"
                  >{{ item.name }}</el-button
                >
                <el-checkbox-group v-model="item.checkList" style="float:left">
                  <el-checkbox
                    v-for="method in item.perm_methods"
                    :key="method.codename"
                    :label="method.codename"
                    >{{ method.name }}</el-checkbox
                  >
                </el-checkbox-group>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>

      <div class="body page">
        <h5>所有用户组</h5>
        <el-divider></el-divider>
      </div>

      <div class="body page">
        <el-row>
          <el-col
            v-for="(item, index) in all_groups"
            :key="index"
            :xs="12"
            :lg="4"
          >
            <el-button-group>
              <el-button
                v-if="index == choosed_group"
                @click="chooseGroup(index)"
                type="warning"
                >{{ item.name }}</el-button
              >
              <el-button v-else @click="chooseGroup(index)" type="primary">{{
                item.name
              }}</el-button>
              <el-button
                @click="deleteGroup(item.name)"
                type="danger"
                icon="el-icon-delete"
              ></el-button>
            </el-button-group>
          </el-col>
        </el-row>
      </div>

      <div class="body page">
        <h5>用户列表</h5>
        <el-divider></el-divider>
      </div>

      <el-row :gutter="10">
        <el-col :span="16">
          <div class="body page">
            <el-transfer
              filterable
              :filter-method="filterMethod"
              filter-placeholder="请输入用户名"
              v-model="choosed_user"
              :data="userlist"
            >
            </el-transfer>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="body page">
            <el-button @click="setUserToGroup()" type="success" round
              >保存分配</el-button
            >
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import Qs from "qs"
export default {
  //   beforeRouteEnter: (to, from, next) => {
  //     let checkInfo = {
  //       contentType: "auth_user",
  //       permissions: ["add", "change", "delete", "view"]
  //     }
  //     store.dispatch("checkUserPerm", checkInfo)
  //     next()
  //   }

  data() {
    return {
      new_group: {
        name: "",
        checkList: [
          {
            name: "文章管理",
            content_type: "blog_article",
            perm_methods: [
              {
                name: "增",
                codename: "add"
              },
              {
                name: "删",
                codename: "delete"
              },
              {
                name: "改",
                codename: "change"
              },
              {
                name: "查",
                codename: "view"
              }
            ],
            checkList: []
          },
          {
            name: "用户管理",
            content_type: "auth_user",
            perm_methods: [
              {
                name: "增",
                codename: "add"
              },
              {
                name: "删",
                codename: "delete"
              },
              {
                name: "改",
                codename: "change"
              },
              {
                name: "查",
                codename: "view"
              }
            ],
            checkList: []
          },
          {
            name: "栏目管理",
            content_type: "blog_category",
            perm_methods: [
              {
                name: "增",
                codename: "add"
              },
              {
                name: "删",
                codename: "delete"
              },
              {
                name: "改",
                codename: "change"
              },
              {
                name: "查",
                codename: "view"
              }
            ],
            checkList: []
          }
        ]
      },
      all_groups: [],

      // 用户列表 分配
      userlist: [],
      choosed_user: [],
      choosed_group: 0,
      filterMethod(query, item) {
        return item.name.indexOf(query) > -1
      }
    }
  },
  mounted() {
    this.getAllUserGroup()
    this.getUserList()
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
    // 保存分配用户与用户组
    setUserToGroup() {
      let group = this.all_groups[this.choosed_group]
      let userlist = this.choosed_user
      if (userlist.length == 0) {
        this.messageNotify("警告", "没有选择用户", "warning")
        return
      }
      // console.log(group)
      // 提交用户组分配
      axios({
        url: "http://127.0.0.1:9000/api/wong-group/",
        method: "post",
        data: Qs.stringify({
          token: this.$store.getters.isnotUserLogin,
          group: group.name,
          userlist: JSON.stringify(userlist)
        })
      }).then(res => {
        console.log(res.data)
        if (res.data == "nologin") {
          this.messageNotify("警告", "尚未登录", "warning")
          return
        }
        if (res.data == "noperm") {
          this.messageNotify("警告", "权限不足", "warning")
          return
        }
        if (res.data == "ok") {
          this.messageNotify("成功", "用户权限分配成功", "success")
          return
        }
      })
    },
    // 选择用户组
    chooseGroup(index) {
      this.choosed_group = index
    },
    // 用户列表
    getUserList() {
      axios({
        url: "http://127.0.0.1:9000/api/wong-userlist/",
        method: "get"
      }).then(res => {
        console.log(res.data)
        let userlist = res.data
        userlist.forEach(user => {
          this.userlist.push({
            label: user.name,
            key: user.name,
            name: user.name
          })
        })
      })
    },
    // 获取所有用户组
    getAllUserGroup() {
      axios({
        url: "http://127.0.0.1:9000/api/wong-group/",
        method: "get"
      }).then(res => {
        console.log(res.data)
        this.all_groups = res.data
      })
    },
    // 删除用户组
    deleteGroup(name) {
      axios({
        url: "http://127.0.0.1:9000/api/wong-group/",
        method: "delete",
        data: Qs.stringify({
          name: name,
          token: this.$store.getters.isnotUserLogin
        }),
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      }).then(res => {
        console.log(res.data)
        if (res.data == "nologin") {
          this.messageNotify("警告", "尚未登录！", "warning")
          return
        }
        if (res.data == "noperm") {
          this.messageNotify("警告", "权限不足！", "warning")
          return
        }
        if (res.data == "ok") {
          this.getAllUserGroup()
        }
      })
    },
    saveNewGroup() {
      // 判断名称输入
      if (this.new_group.name.length == 0) {
        this.messageNotify("警告", "输入新用户名称！", "warning")
        return
      }
      // 判断权限的选择
      // console.log(this.new_group.checkList[0].checkList)
      let checkType = false
      let perm_list = []
      this.new_group.checkList.forEach(obj => {
        if (obj.checkList.length > 0) {
          checkType = true
          let perm_item = {
            content_type: obj.content_type,
            perm_methods: obj.checkList
          }
          perm_list.push(perm_item)
        }
      })
      if (checkType) {
        // 执行提交
        let checkInfo = {
          contentType: "auth_user",
          permissions: ["add", "change", "delete", "view"]
        }
        this.$store.dispatch("checkUserPerm", checkInfo).then(res => {
          if (res) {
            axios({
              url: "http://127.0.0.1:9000/api/wong-group/",
              method: "put",
              data: Qs.stringify({
                token: this.$store.getters.isnotUserLogin,
                new_group: this.new_group.name,
                perm_list: JSON.stringify(perm_list)
              })
            }).then(res => {
              console.log(res.data)
              if (res.data == "nologin") {
                this.messageNotify("警告", "尚未登录！", "warning")
                return
              }
              if (res.data == "noperm") {
                this.messageNotify("警告", "权限不足！", "warning")
                return
              }
              if (res.data == "same name") {
                this.messageNotify("警告", "重复命名！", "warning")
                return
              }
              if (res.data == "ok") {
                this.getAllUserGroup()
              }
            })
          }
        })
      } else {
        this.messageNotify("警告", "新用户组权限未选择！", "warning")
        return
      }
    },
    // 全选 权限多选框
    chooseAllmethod(index) {
      if (this.new_group.checkList[index].checkList.length == 0) {
        this.new_group.checkList[index].checkList = [
          "add",
          "delete",
          "change",
          "view"
        ]
      } else {
        this.new_group.checkList[index].checkList = []
      }
    }
  }
}
</script>

<style scoped>
.page {
  padding: 10px 10px;
}

.new-group {
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.perm-list {
  height: 200px;
  overflow-y: scroll;
}
</style>
