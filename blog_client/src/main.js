import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

//引入summernote
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'
import 'popper.js'
import 'summernote'
import 'summernote/lang/summernote-zh-CN.js'
import 'summernote/dist/summernote.css'
import './assets/css/index.css'
import './assets/iconfont/iconfont.css'

// markdown编辑器
import VMdEditor from '@kangc/v-md-editor'
import VueMarkdownEditor from '@kangc/v-md-editor'
import '@kangc/v-md-editor/lib/style/base-editor.css'
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js'
import '@kangc/v-md-editor/lib/theme/style/vuepress.css'

import githubTheme from '@kangc/v-md-editor/lib/theme/github.js'
import '@kangc/v-md-editor/lib/theme/style/github.css'

import VMdPreview from '@kangc/v-md-editor/lib/preview'
import '@kangc/v-md-editor/lib/style/preview.css'

import hljs from 'highlight.js'
import Prism from 'prismjs'

// 渲染组件
VMdPreview.use(vuepressTheme, {
	Prism,
})

VueMarkdownEditor.use(githubTheme, {
	Hljs: hljs,
})

Vue.use(VMdPreview)
Vue.use(VueMarkdownEditor)
Vue.use(ElementUI)
Vue.config.productionTip = false

new Vue({
	router,
	store,
	render: (h) => h(App),
}).$mount('#app')
