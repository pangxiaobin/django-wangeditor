/* global WANGEDITOR */
;(function () {
    // var el = document.getElementById('wangeditor-init-script');
    // if (el && !window.WANGEDITOR_BASEPATH) {
    //   window.CKEDITOR_BASEPATH = el.getAttribute('data-ckeditor-basepath');
    // }

    // Polyfill from https://developer.mozilla.org/en/docs/Web/API/Element/matches
    if (!Element.prototype.matches) {
        Element.prototype.matches =
            Element.prototype.matchesSelector ||
            Element.prototype.mozMatchesSelector ||
            Element.prototype.msMatchesSelector ||
            Element.prototype.oMatchesSelector ||
            Element.prototype.webkitMatchesSelector ||
            function (s) {
                var matches = (this.document || this.ownerDocument).querySelectorAll(s),
                    i = matches.length;
                while (--i >= 0 && matches.item(i) !== this) {
                }
                return i > -1;
            };
    }

    function runInitialisers() {
        if (!window.wangEditor) {
            setTimeout(runInitialisers, 100);
            return;
        }

        initialiseWangEditor();
        initialiseWangEditorInInlinedForms();
    }

    if (document.readyState !== 'loading' && document.body) {
        document.addEventListener('DOMContentLoaded', initialiseWangEditor);
        runInitialisers();
    } else {
        document.addEventListener('DOMContentLoaded', runInitialisers);
    }

    function initialiseWangEditor() {
        var divs = Array.prototype.slice.call(document.querySelectorAll('div[data-type=wangeditortype]'));
        var textareas = Array.prototype.slice.call(document.querySelectorAll('textarea[data-type=wangtextareas]'));
        var wangeditortype_toolbars = Array.prototype.slice.call(document.querySelectorAll('div[data-type=wangeditorToolbar]'));
        var wangeditortype_container = Array.prototype.slice.call(document.querySelectorAll('div[data-type=wangeditorContainer]'));
        for (var i = 0; i < divs.length; ++i) {
            var d = divs[i];
            var t = textareas[i];
            var tool = wangeditortype_toolbars[i]
            var container = wangeditortype_container[i]
            if (d.getAttribute('data-processed') === '0' && d.id.indexOf('__prefix__') === -1) {
                d.setAttribute('data-processed', '1');
                const {createEditor, createToolbar} = window.wangEditor
                const menutCong = JSON.parse(d.getAttribute('data-menu-conf'));

                const editorConfig = {
                    onChange(editor) {
                        textarea.innerHTML = editor.getHtml();
                    },
                    MENU_CONF: menutCong
                }
                editorConfig.MENU_CONF['uploadVideo']['onFailed'] = function (file, res) {
                    alert(`${file.name} 上传失败`, res['msg'])
                }
                editorConfig.MENU_CONF['uploadImage']['onFailed'] = function (file, res) {
                    alert(`${file.name} 上传失败`, res['msg'])
                }
                const editor = createEditor({
                    selector: '#' + container.id,
                    html: '',
                    config: editorConfig,
                    mode: 'default', // or 'simple'
                })

                editor.on('fullScreen', () => {
                    const stickyElements = document.querySelectorAll('.sticky');
                    stickyElements.forEach(element => {
                        element.style.display = 'none';
                    });
                })
                editor.on('unFullScreen', () => {
                    const stickyElements = document.querySelectorAll('.sticky');
                    stickyElements.forEach(element => {
                        element.style.display = '';
                    });
                })
                const toolbarConfig = JSON.parse(d.getAttribute('data-toolbar-config'));
                const toolbar = createToolbar({
                    editor,
                    selector: '#' + tool.id,
                    config: toolbarConfig,
                    mode: 'default', // or 'simple'
                })
                const textarea = document.getElementById(t.id);
                // const toolbarConfig = JSON.parse(d.getAttribute('data-config'))

                if (textarea.innerHTML.length !== 0) {
                    editor.setHtml(textarea.innerText);
                }
            }
        }
    }

    function initialiseWangEditorInInlinedForms() {
        // 监听首页增加和修改按钮
        document.body.addEventListener('click', function (e) {
            if (e.target && (
                e.target.matches('.add-row a') ||
                e.target.matches('.grp-add-handler')
            )) {
                initialiseWangEditor();
            }
        });
    }

}());
