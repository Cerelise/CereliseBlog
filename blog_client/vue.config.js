module.exports = {
	chainWebpack: (config) => {
		config.plugin('html').tap((args) => {
			args[0].title = 'CereliseBlog'
			return args
		})
	},
	productionSourceMap: false,
}
