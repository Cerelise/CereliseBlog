<template>
  <div id="register-page">
    <div class="page registerbox" @keyup.enter="blogRegister">
      <div class="header">
        新用户注册
        <el-divider></el-divider>
      </div>
      <el-form
        :label-position="labelPosition"
        label-width="80px"
        :model="formData"
      >
        <el-form-item label="用户名">
          <el-input v-model="formData.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="formData.password"></el-input>
        </el-form-item>
        <el-form-item label="重复密码">
          <el-input v-model="formData.repassword"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="blogRegister()" type="success">注册</el-button>
          <el-button @click="toLogin()" type="warning" plain
            >已有账号</el-button
          >
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      labelPosition: "right",
      formData: {
        username: "",
        password: "",
        repassword: ""
      }
    }
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
    toLogin() {
      this.$router.push({ path: "login/" })
    },
    blogRegister() {
      if (
        this.formData.username.length == 0 ||
        this.formData.password.length == 0 ||
        this.formData.repassword.length == 0
      ) {
        this.messageNotify("警告", "帐号或密码不能为空!", "warning")
        // alert('表单未填写完整')
        return
      }
      if (this.formData.password != this.formData.repassword) {
        this.messageNotify("警告", "两次密码不一致!", "warning")
        // alert('两次输入的密码不一致')
        return
      }
      if (
        this.formData.password.length < 7 ||
        this.formData.repassword.length < 7
      ) {
        // alert('密码太短！')
        this.messageNotify("警告", "密码不能低于8位!", "warning")
        return
      }
      this.$store.dispatch("blogRegister", this.formData)
    }
  }
}
</script>

<style>
#register-page {
  height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.registerbox {
  padding: 10px 10px;
}
</style>
