# Frontend

This is the react package to create a webpage displaying data processed by CoroNow's core components.  

## Implementation

### Navigation Side Bar

A sidebar component on the right side, expand on mouse over and collapse on mouse out. This sidebar will tell Main component whether to render News or Sentiment or jsut Wordcloud.  

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

Add a toolbar on the right side, expand on mouse over.  
Clicking on a specific term on nav bar will allow more content to be rendered  
