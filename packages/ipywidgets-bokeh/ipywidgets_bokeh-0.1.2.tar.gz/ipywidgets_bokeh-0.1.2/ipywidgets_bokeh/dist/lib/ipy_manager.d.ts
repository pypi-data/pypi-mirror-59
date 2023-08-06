export declare function require_loader(moduleName: string, moduleVersion: string): Promise<any>;
export declare type WidgetManager = {
    render(bundle: unknown, el: HTMLElement): Promise<unknown>;
    kernel: any;
};
export declare function create_widget_manager(): Promise<WidgetManager>;
