<template>
  <div id="login-page" class="flex">
    <div class="page loginbox">
      <div class="header">
        用户登录
        <el-divider></el-divider>
      </div>
      <el-form
        :label-position="labelPosition"
        label-width="60px"
        :model="formData"
      >
        <el-form-item label="用户名">
          <el-input v-model="formData.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="formData.password" show-password></el-input>
          <div style="display: flex;flex-direction: row-reverse;">
            <a href="" @click.prevent="toResetPwd()" style="color:aqua; "
              >忘记密码?</a
            >
          </div>
        </el-form-item>
        <el-form-item class="login-footer">
          <el-button @click="blogLogin()" type="success">登录</el-button>
          <el-button @click="toRegister()" type="warning" plain
            >前往注册</el-button
          >
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
// import axios from 'axios'
// import Qs from 'qs'
export default {
  data() {
    return {
      labelPosition: "right",
      formData: {
        username: "",
        password: ""
      }
    }
  },
  methods: {
    toRegister() {
      this.$router.push({ path: "/register" })
    },
    toResetPwd() {
      this.$router.push({ path: "/resetpwd" })
    },
    blogLogin() {
      if (
        this.formData.username.length == 0 ||
        this.formData.password.length == 0
      ) {
        // alert("表单未填写完整")
        this.$notify({
          title: "警告",
          message: "账号或密码不能为空！",
          type: "warning",
          showClose: true,
          center: true
        })
        return
      }
      this.$store.dispatch("blogLogin", this.formData)
    }
  }
}
</script>

<style scope>
#login-page {
  height: 80vh;
}

.loginbox {
  padding: 20px;
  height: 50vh;
  width: 40vw;
}

.login-footer {
  display: flex;
  justify-content: center;
}

.el-button {
  margin-right: 20px;
}
</style>
