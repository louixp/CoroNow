import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


function Word(props) {
    let size_str = (5*props.weight).toString() + "px";
    let style_obj = {
        fontSize: size_str,
        padding: "0px",
    };
    console.log(size_str)
    return <button id="word_cloud_bubble" style={style_obj}>{props.text}</button>;
} 


// wordcloud window, a div element, containing a bunch of words
class WordCloud extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "init",
            words: [],
        };
        this.getWordCloud();
    }

    getWordCloud() {
        // fetch a wordcloud json from backend server
        fetch("/api/wordcloud", {
            method: "GET",
            cache: "no-cache",
            headers: {
                "Content-type": "application/json",
            },
            redirect: "follow",
        })
            .then((res) => res.json())
            .then((res) => {
                let new_words = [];
                res.words.forEach(el => {
                    new_words.push(el);
                });
                console.log(new_words);
                this.setState({
                    state: "display",
                    words: new_words,
                });
            });
    }

    render() {
        if (this.state.state === "init") {
            return (
                <div>
                    <Word text='nothing here'/>
                </div>
            )
        }
        else if (this.state.state === "display") {
            return (
                <div>
                    {this.state.words.map(el => <Word text={el.word} weight={el.weight} key={el.word}/>)}
                </div>
            )
        }
    }
}


// main frame of home page
class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "init", // states: init, trial
        }
    }

    render() {
        if (this.state.state === "init") {

            return <WordCloud/>;
        }
    }
}


ReactDOM.render(<Main />, document.getElementById('root'));
