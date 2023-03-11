<template>
  <div id="reset-page" class="flex">
    <div class="page resetbox">
      <div class="header">
        重置密码
        <el-divider />
      </div>
      <el-form
        :label-position="labelPosition"
        label-width="80px"
        :model="formData"
      >
        <el-form-item label="用户名">
          <el-input v-model="formData.username"></el-input>
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="formData.password" show-password></el-input>
        </el-form-item>
        <el-form-item label="重复密码">
          <el-input v-model="formData.repassword" show-password></el-input>
        </el-form-item>
        <el-form-item class="reset-footer">
          <el-button @click="blogResetPwd()" type="success">重置</el-button>
          <el-button @click="toLogin()" type="warning" plain
            >返回登录页面</el-button
          >
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import Qs from "qs"
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
    blogResetPwd() {
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

      if (this.formData.username.length != 0) {
        axios({
          url: this.$store.state.baseUrl + "api/wong-resetpwd/",
          method: "post",
          data: Qs.stringify(this.formData)
        }).then(res => {
          console.log(res.data)
          if (res.data == "not_exist") {
            this.messageNotify("警告", "账号不存在", "warning")
            return
          } else {
            this.messageNotify("成功", "修改成功", "success")
            this.$router.push({ path: "login/" })
          }
        })
      }
    }
  }
}
</script>

<style scoped>
#reset-page {
  height: 80vh;
}
.resetbox {
  padding: 10px 10px;
  height: 50vh;
  width: 40vw;
}

.reset-footer {
  display: flex;
  justify-content: center;
}
</style>
