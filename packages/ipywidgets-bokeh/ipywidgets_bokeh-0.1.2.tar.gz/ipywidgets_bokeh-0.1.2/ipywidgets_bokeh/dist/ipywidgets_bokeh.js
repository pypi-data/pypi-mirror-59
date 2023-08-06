/*!
 * Copyright (c) 2012 - 2019, Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
*/
(function(root, factory) {
  factory(root["Bokeh"]);
})(this, function(Bokeh) {
  var define;
  return (function(modules, entry, aliases, externals) {
    if (Bokeh != null) {
      return Bokeh.register_plugin(modules, entry, aliases, externals);
    } else {
      throw new Error("Cannot find Bokeh. You have to load it prior to loading plugins.");
    }
  })
({
"8a0dda95db": /* index.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    const ipy_widget_1 = require("4391b7d8b0") /* ./ipy_widget */;
    const base_1 = require("@bokehjs/base");
    base_1.register_models({ IPyWidget: ipy_widget_1.IPyWidget });
},
"4391b7d8b0": /* ipy_widget.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    const tslib_1 = require("tslib");
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    const events_1 = require("@bokehjs/document/events");
    const p = tslib_1.__importStar(require("@bokehjs/core/properties"));
    const ipy_manager_1 = require("940dc34b97") /* ./ipy_manager */;
    const widget_managers = new WeakMap();
    class IPyWidgetView extends html_box_1.HTMLBoxView {
        constructor() {
            super(...arguments);
            this.rendered = false;
        }
        render() {
            super.render();
            if (!this.rendered) {
                this._render().then(() => {
                    this.rendered = true;
                    this.invalidate_layout();
                    this.notify_finished();
                });
            }
        }
        has_finished() {
            return this.rendered && super.has_finished();
        }
        async _render() {
            const manager = await widget_managers.get(this.model.document);
            await manager.render(this.model.bundle, this.el);
        }
    }
    exports.IPyWidgetView = IPyWidgetView;
    IPyWidgetView.__name__ = "IPyWidgetView";
    class IPyWidget extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_IPyWidget() {
            this.prototype.default_view = IPyWidgetView;
            this.define({
                bundle: [p.Any],
            });
        }
        _doc_attached() {
            const doc = this.document;
            let widget_manager = widget_managers.get(doc);
            if (widget_manager == null) {
                widget_manager = ipy_manager_1.create_widget_manager();
                widget_managers.set(doc, widget_manager);
                widget_manager.then((manager) => {
                    manager.kernel.bk_send = (data) => {
                        const event = new events_1.MessageSentEvent(doc, "ipywidgets_bokeh", data);
                        doc._trigger_on_change(event);
                    };
                    doc.on_message("ipywidgets_bokeh", (data) => {
                        manager.kernel.bk_recv({ data });
                    });
                });
            }
        }
    }
    exports.IPyWidget = IPyWidget;
    IPyWidget.__name__ = "IPyWidget";
    IPyWidget.__module__ = "ipywidgets_bokeh.ipy_widget";
    IPyWidget.init_IPyWidget();
},
"940dc34b97": /* ipy_manager.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    function require_promise(pkg) {
        return new Promise((resolve, reject) => requirejs(pkg, resolve, reject));
    }
    const cdn = 'https://unpkg.com';
    function get_cdn_url(moduleName, moduleVersion) {
        let packageName = moduleName;
        let fileName = 'index'; // default filename
        // if a '/' is present, like 'foo/bar', packageName is changed to 'foo', and path to 'bar'
        // We first find the first '/'
        let index = moduleName.indexOf('/');
        if ((index != -1) && (moduleName[0] == '@')) {
            // if we have a namespace, it's a different story
            // @foo/bar/baz should translate to @foo/bar and baz
            // so we find the 2nd '/'
            index = moduleName.indexOf('/', index + 1);
        }
        if (index != -1) {
            fileName = moduleName.substr(index + 1);
            packageName = moduleName.substr(0, index);
        }
        return `${cdn}/${packageName}@${moduleVersion}/dist/${fileName}`;
    }
    const mods = new Set();
    function require_loader(moduleName, moduleVersion) {
        if (!mods.has(moduleName)) {
            mods.add(moduleName);
            const conf = { paths: {} };
            conf.paths[moduleName] = get_cdn_url(moduleName, moduleVersion);
            requirejs.config(conf);
        }
        console.log(`Loading ${moduleName}@${moduleVersion} from ${cdn}`);
        return require_promise([moduleName]);
    }
    exports.require_loader = require_loader;
    async function create_widget_manager() {
        const { WidgetManager } = await require_promise(["@bokeh/jupyter_embed"]);
        return new WidgetManager({ loader: require_loader });
    }
    exports.create_widget_manager = create_widget_manager;
},
}, "8a0dda95db", {"index":"8a0dda95db","ipy_widget":"4391b7d8b0","ipy_manager":"940dc34b97"}, {});
})

//# sourceMappingURL=ipywidgets_bokeh.js.map
