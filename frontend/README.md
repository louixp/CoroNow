# Frontend

This is the react package to create a webpage displaying data processed by CoroNow's core components.  

## Implementation

### Word Cloud

Use react-wordcloud package to create a responsive, callback-able wordcloud.  
NOTES

* big font size may lead to severe performance drop  

* shouldComponentUpdate() method is buggy, need to move wordcloud update method to Main component to control wordcloud version  

### Word Trend

Use react-bootstrap to create an Modal component displaying trend information.  
NOTES

* when modal/overlay is rendered, wordcloud will also be re-rendered. should be solved by enforcing a will function.  

### Sentiments

Desired effect: when scrolling down along the page, word cloud shrinks vertically, and giving about 2/3 of the space of the whole page to sentiment results.  
TODO  
