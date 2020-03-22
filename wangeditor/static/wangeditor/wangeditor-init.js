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
        for (var i = 0; i < divs.length; ++i) {
            var d = divs[i];
            var t = textareas[i];
            if (d.getAttribute('data-processed') === '0' && d.id.indexOf('__prefix__') === -1) {
                d.setAttribute('data-processed', '1');
                var E = window.wangEditor;
                var editor = new E(document.getElementById(d.id));
                const textarea = document.getElementById(t.id);
                editor.customConfig = JSON.parse(d.getAttribute('data-config'));
                editor.customConfig.onchange = function (html) {
                    // 监控变化，同步更新到 textarea
                    textarea.innerHTML = html;
                };
                editor.customConfig.uploadImgHooks = {
                     fail: function (xhr, editor, result) {
                    // 图片上传并返回结果，但图片插入错误时触发
                    // xhr 是 XMLHttpRequst 对象，editor 是编辑器对象，result 是服务器端返回的结果
                     if (result['errno'] !== 0){
                         alert(result['msg'])
                     }
                },
                };
                editor.create();
                if (textarea.innerHTML.length !== 0) {
                    editor.txt.html(textarea.innerText);

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
