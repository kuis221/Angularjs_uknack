module.exports = function(grunt) {
	// probably only will use imagemin - spritesmith 
	grunt.loadNpmTasks('grunt-spritesmith');
	
	grunt.initConfig({
		sprite:{
			all: {
				src: 'images/sprites-images/*.png',
				dest: 'images/sprites/sprites.png',
				destCss: 'css/sprites.css'
			}
		}
	});
	
	// register tasks
    grunt.registerTask('default', [
        'sprite'
    ]);
	
};