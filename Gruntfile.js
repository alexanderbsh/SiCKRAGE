module.exports = function (grunt) {
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        clean: {
            bower_components: 'bower_components',
            //sass: [
            //    '.sass-cache',
            //    'sickrage/core/webserver/gui/default/scss/'
            //],
            options: {
                force: true
            }
        },
        bower: {
            install: {
                options: {
                    copy: false
                }
            }
        },
        bower_concat: {
            all: {
                dest: {
                    js: 'dist/js/bower.js',
                    css: 'dist/css/bower.css'
                },
                callback: function (mainFiles) {
                    return mainFiles.map(function (filepath) {
                        var min = filepath.replace(/\.js$/, '.min.js');
                        return grunt.file.exists(min) ? min : filepath;
                    });
                },
                mainFiles: {
                    'bootstrap': [
                        'dist/css/bootstrap.min.css',
                        'dist/js/bootstrap.min.js'
                    ],
                    'bootstrap-formhelpers': [
                        'dist/js/bootstrap-formhelpers.min.js',
                        'dist/css/bootstrap-formhelpers.min.css'
                    ],
                    'jquery-ui': [
                        'jquery-ui.min.js',
                        'themes/base/jquery-ui.min.css'
                    ],
                    'jquery.tablesorter': [
                        'dist/js/jquery.tablesorter.js',
                        'dist/js/widgets/widget-columnSelector.min.js',
                        'dist/js/widgets/widget-stickyHeaders.min.js',
                        'dist/js/widgets/widget-reflow.min.js',
                        'dist/js/widgets/widget-filter.min.js',
                        'dist/js/widgets/widget-saveSort.min.js',
                        'dist/js/widgets/widget-storage.min.js',
                        'dist/css/theme.blue.css'
                    ],
                    'isotope': [
                        "dist/isotope.pkgd.min.js"
                    ],
                    'jquery-json': [
                        'dist/jquery.json.min.js'
                    ],
                    'pnotify': [
                        'dist/pnotify.js',
                        'dist/pnotify.desktop.js',
                        'dist/pnotify.nonblock.js',
                        'dist/pnotify.css'
                    ],
                    "outlayer": [
                        "item.js",
                        "outlayer.js"
                    ],
                    "bootstrap-tokenfield": [
                        "dist/bootstrap-tokenfield.js",
                        "dist/css/tokenfield-typeahead.css",
                        "dist/css/bootstrap-tokenfield.css"
                    ]
                },
                bowerOptions: {
                    relative: false
                },
                dependencies: {
                    'selectboxes': 'jquery',
                    'bookmarkscroll': 'jquery'
                }
            }
        },
        googlefonts: {
            build: {
                options: {
                    fontPath: 'sickrage/core/webserver/gui/default/fonts/',
                    cssFile: 'dist/css/fonts.css',
                    httpPath: '/fonts/',
                    formats: {
                        eot: true,
                        ttf: true,
                        woff: true,
                        woff2: true,
                        svg: true
                    },
                    fonts: [
                        {
                            family: 'Open Sans',
                            styles: [
                                300, '300italic',
                                400, '400italic',
                                600, '600italic',
                                700, '700italic',
                                800, '800italic'
                            ]
                        },
                        {
                            family: 'Droid Sans',
                            styles: [
                                400, 700
                            ]
                        }
                    ]
                }
            }
        },
        copy: {
            glyphicon: {
                files: [{
                    expand: true,
                    flatten: true,
                    cwd: 'bower_components/bootstrap/fonts/',
                    src: ['**/*.{eot,svg,ttf,woff,woff2}'],
                    dest: 'sickrage/core/webserver/gui/default/fonts/'
                }]
            }
        },
        imagemin: {
            jquery_ui: {
                files: [{
                    expand: true,
                    flatten: true,
                    cwd: 'bower_components/jquery-ui/themes/',
                    src: ['**/*.{png,jpg,gif}'],
                    dest: 'sickrage/core/webserver/gui/default/images/'
                }]
            },
            tablesorter: {
                files: [{
                    expand: true,
                    flatten: true,
                    cwd: 'bower_components/jquery.tablesorter/dist/css/images/',
                    src: ['**/*.{png,jpg,gif}'],
                    dest: 'sickrage/core/webserver/gui/default/images/tablesorter/'
                }]
            },
            boostrap_formhelpers: {
                files: [{
                    expand: true,
                    flatten: true,
                    cwd: 'bower_components/bootstrap-formhelpers/img/',
                    src: ['**/*.{png,jpg,gif}'],
                    dest: 'sickrage/core/webserver/gui/default/images/bootstrap-formhelpers/'
                }]
            }
        },
        sprite: {
            icons_sickrage: {
                src: 'dist/images/icons/sickrage/*.png',
                dest: 'sickrage/core/webserver/gui/default/images/icons-sickrage.png',
                destCss: 'dist/css/icons-sickrage.css',
                imgPath: '../images/icons-sickrage.png',
                cssTemplate: 'dist/css/icons-sickrage.css.handlebars',
                padding: 2
            }
        },
        uglify: {
            bower: {
                files: {
                    'sickrage/core/webserver/gui/default/js/bower.min.js': ['dist/js/bower.js']
                }
            },
            core: {
                files: {
                    'sickrage/core/webserver/gui/default/js/core.min.js': ['dist/js/core.js']
                }
            }
        },
        sass: {
            core: {
                files: {
                    'sickrage/core/webserver/gui/default/scss/core.scss': [
                        'dist/css/core.css',
                        'dist/css/fonts.css',
                        'dist/css/icons-sickrage.css'
                    ]
                }
            }
        },
        cssmin: {
            options: {
                shorthandCompacting: false,
                roundingPrecision: -1
            },
            bower: {
                files: {
                    'sickrage/core/webserver/gui/default/css/bower.min.css': ['dist/css/bower.css']
                }
            },
            core: {
                files: {
                    'sickrage/core/webserver/gui/default/css/core.min.css': [
                        'dist/css/core.css',
                        'dist/css/fonts.css',
                        'dist/css/icons-sickrage.css'
                    ],
                    'sickrage/core/webserver/gui/default/css/themes/dark.min.css': [
                        'dist/css/themes/dark.css'
                    ],
                    'sickrage/core/webserver/gui/default/css/themes/light.min.css': [
                        'dist/css/themes/light.css'
                    ]
                }
            }
        },
        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            all: ['dist/js/core.js']
        },
        changelog: {
            release: {
                options: {
                    after: '256',
                    logArguments: [
                        '--pretty=* %h - %ad: %s',
                        '--no-merges',
                        '--date=short'
                    ],
                    fileHeader: '# Changelog',
                    featureRegex: /^(.*)$/gim,
                    partials: {
                        features: '{{#each features}}{{> feature}}{{/each}}\n',
                        feature: '- {{this}} {{this.date}}\n',
                        fixes: '{{#each fixes}}{{> fix}}{{/each}}\n',
                        fix: '- {{this}} {{this.date}}\n'

                    },
                    dest: "changelog.md"
                }
            }
        }
    });

    grunt.registerTask(
        'default', [
            'clean',
            'bower',
            'bower_concat',
            'googlefonts',
            'copy',
            'imagemin',
            'uglify',
            'sprite',
            'sass',
            'cssmin',
            'jshint'
        ]
    );
};