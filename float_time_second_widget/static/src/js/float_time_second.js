/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useNumpadDecimal } from "@web/views/fields/numpad_decimal_hook";
import { Component } from "@odoo/owl";

/**
 * Convert float hours into HH:MM:SS format
 */
export function formatFloatTimeSeconds(value) {
    if (typeof value !== "number" || isNaN(value) || value === false) {
        return "00:00:00";
    }

    const isNegative = value < 0;
    value = Math.abs(value);

    const totalSeconds = Math.round(value * 3600);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    const sign = isNegative ? "-" : "";
    return `${sign}${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

/**
 * Convert HH:MM:SS string into float hours
 */
export function parseFloatTimeSeconds(value) {
    if (!value || typeof value !== "string") {
        return 0;
    }
    value = value.trim();
    if (value === "") {
        return 0;
    }
    let sign = 1;
    if (value.startsWith("-")) {
        value = value.slice(1);
        sign = -1;
    }
    const values = value.split(":");
    if (values.length > 3) {
        throw new Error(`"${value}" is not a valid time format`);
    }

    if (values.length === 1) {
        const parsed = Number(values[0]);
        if (isNaN(parsed)) {
            throw new Error(`"${value}" is not a valid time format`);
        }
        return sign * parsed;
    }

    const hours = parseInt(values[0], 10);
    const minutes = parseInt(values[1], 10);
    const seconds = values.length === 3 ? parseInt(values[2], 10) : 0;

    if (isNaN(hours) || isNaN(minutes) || isNaN(seconds)) {
        throw new Error(`"${value}" is not a valid time format`);
    }

    return sign * (hours + minutes / 60 + seconds / 3600);
}

export class FloatTimeSecondField extends Component {
    static template = "float_time_second_widget.FloatTimeSecondField";
    static props = {
        ...standardFieldProps,
        inputType: { type: String, optional: true },
        placeholder: { type: String, optional: true },
    };
    static defaultProps = {
        inputType: "text",
    };

    setup() {
        useInputField({
            getValue: () => this.formattedValue,
            refName: "numpadDecimal",
            parse: (v) => parseFloatTimeSeconds(v),
        });
        useNumpadDecimal();
    }

    get formattedValue() {
        const value = this.props.record.data[this.props.name];
        return formatFloatTimeSeconds(value);
    }
}

export const floatTimeSecondField = {
    component: FloatTimeSecondField,
    displayName: _t("Time with Seconds"),
    supportedOptions: [
        {
            label: _t("Type"),
            name: "type",
            type: "string",
            default: "text",
        },
    ],
    supportedTypes: ["float"],
    isEmpty: () => false,
    extractProps: ({ attrs, options, placeholder }) => ({
        inputType: options.type,
        placeholder: placeholder || attrs?.placeholder,
    }),
};

registry.category("fields").add("float_time_second", floatTimeSecondField);
