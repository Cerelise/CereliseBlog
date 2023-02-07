import Vue from "vue"
import Vuex from "vuex"
import axios from "axios"
import Qs from "qs"
import router from "../router"
import { Notification } from "element-ui"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentname: "",
    loginmessage: "",
    userinfo: {}
  },
  getters: {
    // 查询登录状态
    isnotUserLogin(state) {
      return state.userinfo.token
    }
  },
  mutations: {
    // 保存注册登录用户信息
    saveUserinfo(state, userinfo) {
      state.userinfo = userinfo
    },
    // 清空用户登录状态
    clearUserinfo(state) {
      state.userinfo = {}
    }
  },
  actions: {
    // 登录
    blogLogin({ commit }, formData) {
      axios({
        url: "http://127.0.0.1:9000/api/wong-login/",
        method: "post",
        data: Qs.stringify(formData)
      }).then(res => {
        if (res.data == "none") {
          Notification({
            title: "错误",
            message: "用户不存在！",
            type: "error"
          })
          return
        }
        if (res.data == "pwd err") {
          Notification({
            title: "错误",
            message: "密码错误！",
            type: "error"
          })
          return
        }
        // console.log(res.data)
        commit("saveUserinfo", res.data)
        localStorage.setItem("token", res.data.token)
        this.state.currentname = res.data.nickname
        router.push({ path: "/" })
      })
    },

    // 注册
    blogRegister({ commit }, formData) {
      axios({
        url: "http://127.0.0.1:9000/api/wong-register/",
        method: "post",
        data: Qs.stringify(formData)
      }).then(res => {
        if (res.data == "repeat") {
          // alert("用户名已存在！")
          Notification({
            title: "警告",
            message: "用户已注册！",
            type: "warning"
          })
          return
        }
        console.log(res.data)
        commit("saveUserinfo", res.data)
        // 缓存
        localStorage.setItem("token", res.data.token)
        this.state.currentname = res.data.nickname
        router.push({ path: "/" })
      })
    },
    // 自动登录
    tryAutoLogin({ commit }) {
      let token = localStorage.getItem("token")
      this.state.currentname = localStorage.getItem("username")
      if (token) {
        axios({
          url: "http://127.0.0.1:9000/api/wong-autologin/",
          method: "post",
          data: Qs.stringify({ token })
        }).then(res => {
          // console.log(res.data)
          if (res.data == "tokenTimeout") {
            Notification({
              title: "错误",
              message: "用户信息过期，请重新登录!",
              type: "error"
            })
            return
          }
          commit("saveUserinfo", res.data)
          // 缓存
          localStorage.setItem("token", res.data.token)
          this.state.currentname = res.data.nickname
          router.push({ path: "/" })
        })
      }
    },
    // 登出
    blogLogout({ commit }, token) {
      commit("clearUserinfo")
      localStorage.removeItem("token")
      localStorage.removeItem("username")
      // router.push({ path: "/" })
      axios({
        url: "http://127.0.0.1:9000/api/wong-logout/",
        method: "post",
        data: Qs.stringify({ token })
      }).then(res => {
        console.log(res.data)
      })
    },
    // 权限判断
    async checkUserPerm({ getters }, checkInfo) {
      // 用户
      let token = getters.isnotUserLogin
      // 表
      let contentType = checkInfo.contentType
      // 权限
      let permissions = checkInfo.permissions
      // 鉴权结果
      let perm_data
      await axios({
        url: "http://127.0.0.1:9000/api/wong-checkperm/",
        method: "post",
        data: Qs.stringify({
          token,
          contentType,
          permissions: JSON.stringify(permissions)
        })
      }).then(res => {
        // console.log(res.data)
        if (res.data == "nologin") {
          perm_data = false
          Notification({
            title: "错误",
            message: "用户信息错误",
            type: "error"
          })
          // alert("用户信息错误")
          return
        }
        if (res.data == "noperm") {
          perm_data = false
          Notification({
            title: "错误",
            message: "此用户没有权限,请联系管理员",
            type: "error"
          })
          // alert("此用户没有权限,请联系管理员")
          return
        }
        if (res.data == "ok") {
          perm_data = true
        }
      })
      return perm_data
    }
  },
  modules: {}
})
