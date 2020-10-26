import markdown from '../README.md';
import marked from 'marked';

const html = marked(markdown);
document.querySelector('main').innerHTML = html;