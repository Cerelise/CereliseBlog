<template>
	<div id="user">
		<div class="dweb nav">
			<el-breadcrumb separator-class="el-icon-arrow-right">
				<el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
				<el-breadcrumb-item>用户列表</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="body">
			<!-- <div class="dweb">
        <h5>新建用户组</h5>
        <el-divider></el-divider>
      </div> -->
			<el-row :gutter="10">
				<el-col :xs="24" :lg="12">
					<div class="new-group dweb">
						<el-form :inline="true" :model="new_group" class="demo-form-inline">
							<el-form-item>
								<el-input
									v-model="new_group.name"
									placeholder="新用户组名称"
								></el-input>
							</el-form-item>
							<el-form-item>
								<el-button type="primary" @click="saveNewGroup()"
									>保存</el-button
								>
							</el-form-item>
						</el-form>
					</div>
				</el-col>
				<el-col :xs="24" :lg="12">
					<div class="perm_list dweb">
						<el-row>
							<el-col
								v-for="(item, index) in new_group.checkList"
								:key="index"
								:span="24"
							>
								<el-button
									@click="chooseAllMethod(index)"
									type="primary"
									plain
									style="
										float: left;
										margin-right: 40px;
										margin-top: 10px;
										margin-left: 90px;
									"
									>{{ item.name }}</el-button
								>
								<el-checkbox-group
									v-model="item.checkList"
									style="float: left; margin-top: 20px"
								>
									<el-checkbox
										v-for="method in item.perm_methods"
										:key="method.codename"
										:label="method.codename"
									>
										{{ method.name }}
									</el-checkbox>
								</el-checkbox-group>
							</el-col>
						</el-row>
					</div>
				</el-col>
			</el-row>
		</div>
		<div class="body dweb flex">
			<h5>所有用户组</h5>
		</div>
		<div class="body dweb">
			<el-row class="flex" style="flex-wrap: wrap">
				<el-col
					:xs="12"
					:lg="4"
					v-for="(item, index) in all_groups"
					:key="index"
				>
					<el-button-group class="flex">
						<el-button
							v-if="index == choosed_group"
							@click="choosedGroup(index)"
							type="warning"
							>{{ item.name }}</el-button
						>
						<el-button v-else @click="choosedGroup(index)" type="primary">{{
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
		<div class="body dweb flex">
			<h5>用户列表</h5>
		</div>
		<el-row :gutter="10">
			<el-col :span="24">
				<div class="body dweb perm-flex">
					<el-transfer
						filterable
						:filter-method="filterMethod"
						filter-placeholder="请输入用户名"
						v-model="choosed_user"
						:data="userlist"
					>
					</el-transfer>
					<div class="saveCollections">
						<el-button @click="setUserToGroup()" type="success" plain
							>保存分配</el-button
						>
					</div>
				</div>
			</el-col>
		</el-row>
		<!-- <el-row>
      <el-col :span="24">
        <div class="body dweb flex">
          <el-button @click="setUserToGroup()" type="success" plain>保存分配</el-button>
        </div>
      </el-col>
    </el-row> -->
	</div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'
export default {
	data() {
		return {
			new_group: {
				name: '',
				ame: '',
				checkList: [
					{
						name: '文章管理',
						content_type: 'Blog_article',
						perm_methods: [
							{
								name: '增',
								codename: 'add',
							},
							{
								name: '删',
								codename: 'delete',
							},
							{
								name: '改',
								codename: 'change',
							},
							{
								name: '查',
								codename: 'view',
							},
						],
						checkList: [],
					},
					{
						name: '用户管理',
						content_type: 'auth_user',
						perm_methods: [
							{
								name: '增',
								codename: 'add',
							},
							{
								name: '删',
								codename: 'delete',
							},
							{
								name: '改',
								codename: 'change',
							},
							{
								name: '查',
								codename: 'view',
							},
						],
						checkList: [],
					},
					{
						name: '栏目管理',
						content_type: 'Blog_lanmu',
						perm_methods: [
							{
								name: '增',
								codename: 'add',
							},
							{
								name: '删',
								codename: 'delete',
							},
							{
								name: '改',
								codename: 'change',
							},
							{
								name: '查',
								codename: 'view',
							},
						],
						checkList: [],
					},
				],
			},
			all_groups: [],
			userlist: [],
			choosed_user: [],
			choosed_group: 0,
			filterMethod(query, item) {
				return item.name.indexOf(query) > -1
			},
		}
	},
	mounted() {
		this.getAllUserGroup()
		this.getUserList()
	},
	methods: {
		//提示框
		messageNotify(title, message, type) {
			this.$notify({
				title: title,
				message: message,
				type: type,
				showClose: true,
				center: true,
			})
		},
		// 保存用户分配 用户组
		setUserToGroup() {
			let group = this.all_groups[this.choosed_group]
			let userlist = this.choosed_user
			if (userlist.length == 0) {
				this.messageNotify('警告', '没有选择用户!', 'warning')
				return
			}
			axios({
				url: this.$store.state.baseurl + 'api/azrael-group/',
				method: 'POST',
				data: Qs.stringify({
					token: this.$store.getters.loginState,
					group: group.name,
					userlist: JSON.stringify(userlist),
				}),
			}).then((res) => {
				if (res.data == 'nologin') {
					this.messageNotify('警告', '尚未登录!', 'warning')
					return
				}
				if (res.data == 'noperm') {
					this.messageNotify('警告', '权限不足!', 'warning')
					return
				}
				if (res.data == 'OK') {
					this.messageNotify('成功', '用户权限分配成功!', 'success')
					return
				}
			})
		},
		// 选择用户组
		choosedGroup(index) {
			this.choosed_group = index
		},
		// 获取用户列表
		getUserList() {
			axios({
				url: this.$store.state.baseurl + 'api/azrael-userlist/',
				method: 'GET',
			}).then((res) => {
				let userlist = res.data
				userlist.forEach((user) => {
					this.userlist.push({
						label: user.name,
						key: user.name,
						name: user.name,
					})
				})
			})
		},
		// 获取所有用户组
		getAllUserGroup() {
			axios({
				url: this.$store.state.baseurl + 'api/azrael-group/',
				method: 'GET',
			}).then((res) => {
				this.all_groups = res.data
			})
		},
		// 删除用户组
		deleteGroup(name) {
			axios({
				url: this.$store.state.baseurl + 'api/azrael-group/',
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
				data: Qs.stringify({
					token: this.$store.getters.loginState,
					name: name,
				}),
			}).then((res) => {
				if (res.data == 'nologin') {
					this.messageNotify('警告', '尚未登录!', 'warning')
					return
				}
				if (res.data == 'noperm') {
					this.messageNotify('警告', '权限不足!', 'warning')

					return
				}
				if (res.data == 'OK') {
					this.getAllUserGroup()
				}
			})
		},
		saveNewGroup() {
			//判断名称输入
			if (this.new_group.name.length == 0) {
				this.messageNotify('警告', '输入新用户名称!', 'warning')
				return
			}
			//判断权限的选择
			let checkType = false
			let perm_list = []
			this.new_group.checkList.forEach((obj) => {
				if (obj.checkList.length > 0) {
					checkType = true
					let perm_item = {
						content_type: obj.content_type,
						perm_methods: obj.checkList,
					}
					perm_list.push(perm_item)
				}
			})
			if (checkType) {
				//执行提交
				let checkInfo = {
					contentType: 'auth_user',
					permissions: ['add', 'change', 'delete', 'view'],
				}
				this.$store.dispatch('checkUserPerm', checkInfo).then((res) => {
					if (res) {
						axios({
							url: this.$store.state.baseurl + 'api/azrael-group/',
							method: 'PUT',
							data: Qs.stringify({
								token: this.$store.getters.loginState,
								new_group: this.new_group.name,
								perm_list: JSON.stringify(perm_list),
							}),
						}).then((res) => {
							if (res.data == 'nologin') {
								this.messageNotify('警告', '尚未登录!', 'warning')
								return
							}
							if (res.data == 'noperm') {
								this.messageNotify('警告', '权限不足!', 'warning')
								return
							}
							if (res.data == 'same name') {
								this.messageNotify('警告', '重复命名!', 'warning')
								return
							}
							if (res.data == 'OK') {
								this.getAllUserGroup()
								this.messageNotify('成功', '新用户组保存成功', 'success')
							}
						})
					}
				})
			} else {
				this.messageNotify('警告', '新用户组 权限未选择!!', 'warning')
				return
			}
		},
		// 全选权限多选框
		chooseAllMethod(index) {
			if (this.new_group.checkList[index].checkList.length == 0) {
				this.new_group.checkList[index].checkList = [
					'add',
					'delete',
					'change',
					'view',
				]
			} else {
				this.new_group.checkList[index].checkList = []
			}
		},
	},
}
</script>

<style scoped>
.perm-flex {
	display: flex;
	justify-content: center;
	align-content: center;
	justify-items: center;
	align-items: center;
	flex-direction: column;
}
.flex {
	display: flex;
	justify-content: center;
	justify-items: center;
}
#user .dweb {
	padding: 10px;
}

.nav {
	padding: 25px 10px !important;
}
.body.dweb {
	margin-top: 10px;
}
.body.dweb h5 {
	color: #fff;
	font-weight: 500;
}
.dweb h5 {
	margin-top: 10px;
}
.body .dweb:first-child {
	margin-top: 10px;
	color: #fff;
}
.el-divider--horizontal {
	margin: 0 0;
}
.new-group {
	height: 200px;
	display: flex;
	justify-content: center;
	align-items: center;
}
.perm_list {
	height: 200px;
	display: flex;
	justify-content: center;
	align-content: center;
}

.saveCollections {
	margin-top: 10px;
}
</style>
