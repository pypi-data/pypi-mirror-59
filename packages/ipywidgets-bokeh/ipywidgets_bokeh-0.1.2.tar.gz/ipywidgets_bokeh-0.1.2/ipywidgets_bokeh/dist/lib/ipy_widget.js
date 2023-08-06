import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import { MessageSentEvent } from "@bokehjs/document/events";
import * as p from "@bokehjs/core/properties";
import { create_widget_manager } from "./ipy_manager";
const widget_managers = new WeakMap();
export class IPyWidgetView extends HTMLBoxView {
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
IPyWidgetView.__name__ = "IPyWidgetView";
export class IPyWidget extends HTMLBox {
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
            widget_manager = create_widget_manager();
            widget_managers.set(doc, widget_manager);
            widget_manager.then((manager) => {
                manager.kernel.bk_send = (data) => {
                    const event = new MessageSentEvent(doc, "ipywidgets_bokeh", data);
                    doc._trigger_on_change(event);
                };
                doc.on_message("ipywidgets_bokeh", (data) => {
                    manager.kernel.bk_recv({ data });
                });
            });
        }
    }
}
IPyWidget.__name__ = "IPyWidget";
IPyWidget.__module__ = "ipywidgets_bokeh.ipy_widget";
IPyWidget.init_IPyWidget();
//# sourceMappingURL=ipy_widget.js.map