import markdown from '../README.md';
import marked from 'marked';
import hljs from 'highlight.js/lib/core';
import python from 'highlight.js/lib/languages/python';
import 'highlight.js/styles/github.css';
hljs.registerLanguage('python', python);

const html = marked(markdown);
document.querySelector('main').innerHTML = html;

document.querySelectorAll('pre code').forEach((block) => {
    hljs.highlightBlock(block);
});