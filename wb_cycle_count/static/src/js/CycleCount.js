
/** @odoo-module **/

import core from 'web.core';

const { Component } = owl;
const { useRef, useState, onMounted } = owl.hooks;

class CycleCount extends Component {
        
}

CycleCount.template = "wb_cycle_count.CycleCountTemplate"

core.action_registry.add("wb_cycle_count.wb_cycle_count_scan", CycleCount);
