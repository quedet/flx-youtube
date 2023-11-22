// This is the scss entry file
import "../styles/index.scss";
import "@hotwired/turbo";
import { Application} from "@hotwired/stimulus";
import {definitionsFromContext} from "@hotwired/stimulus-webpack-helpers";
import { Dropdown, Toggle, Alert } from "tailwindcss-stimulus-components";
import ReadMore from 'stimulus-read-more';
import TextareaAutogrow from 'stimulus-textarea-autogrow';
import CheckboxSelectAll from 'stimulus-checkbox-select-all';

window.Stimulus = Application.start();
const context = require.context('../controllers', true, /\.js$/);
window.Stimulus.load(definitionsFromContext(context));

window.Stimulus.register('dropdown', Dropdown);
window.Stimulus.register('toggle', Toggle);
window.Stimulus.register('alert', Alert);
window.Stimulus.register('read-more', ReadMore);
window.Stimulus.register('textarea-autogrow', TextareaAutogrow);
window.Stimulus.register('checkbox-select-all', CheckboxSelectAll);
