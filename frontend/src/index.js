import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import "bootstrap/dist/css/bootstrap.css"; // this file is required for Modal to work
import WordCloud from "./wordcloud.js";
import Wordtrend from "./wordtrend.js";
import Newslist from "./newslist.js";
import Trend from "./trend.js";
import Sidebar from "react-sidebar";
import Nav from "./nav.js";
import Sentiments from "./sentiments.js";

// main frame of home page
class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      trend_open: false,
      sidebar_open: false,
      overlay_text: "",
      word_list_version: 0, // if there's need to update word list, increment this variable to notify wordcloud re-render
      words: [],
      current_trend: [],
      sentiment_list: {},
    };
    this.getWordList();
    this.getSentiments();
  }

  getWordList() {
    // fetch a wordcloud json from backend server
    fetch("/api/wordcloud", {
      method: "GET",
      cache: "no-cache",
      headers: {
        "Content-type": "application/json"
      },
      redirect: "follow"
    })
      .then(res => res.json())
      .then(res => {
        console.log(res);
        this.setState({
          word_list_version: this.state.word_list_version + 1,
          words: res.words
        });
      });
  }

  setSidebarOpen() {
    this.setState({
      sidebar_open: true
    });
  }

  setSidebarClosed() {
    this.setState({
      sidebar_open: false
    });
  }

  sideBarStyle = {
    sidebar: {
      background: "white"
    }
  };

  childSideBar = (
    <div
      className="child-side-bar"
      // onMouseLeave={() => this.setSidebarClosed()}
      style={{
        height: "100%",
        width: "100%",
        textAlign: "center",
        color: "grey",
        fontFamily: "helvetica"
      }}
      onMouseOver={() => this.setSidebarOpen()}
    >
      <p> >> </p>
    </div>
  );

  parentSideBar = (
    <Nav
      onMouseLeave={() => this.setSidebarClosed()}
      style={{
        height: "100%",
        width: "100%"
      }}
      items={[
        {
          text: "WORD CLOUD",
          id: "word-cloud"
        },
        {
          text: "SEARCH NEWS",
          id: "news_list"
        },
        {
          text: "SENTIMENTS",
          id: "sentiments"
        }
      ]}
      callbacks={{
        closeNav: () => this.setSidebarClosed()
      }}
    />
  );

  // callback function for word clicking, display a trend overlay window
  activateTrend(text) {
    // fetch data here
    var that = this;
    var esc = encodeURIComponent;
    var url = "/trend" + "?word=" + esc(text);
    fetch(url, {
      method: "GET",
      cache: "no-cache",
      headers: {
        "Content-type": "application/json"
      },
      redirect: "follow"
    })
      .then(res => res.json())
      .then(res => {
        if (that.state.trend_open === false) {
          that.setState({
            current_trend: res
          });
        }
      })
      .then(() => {
        that.setState({
          trend_open: true,
          overlay_text: text
        });
      });
  }

  // callback function for close window button on overlay, deactivate overlay window
  deactivateTrend() {
    this.setState({
      trend_open: false
    });
  }

  // get sentiments
  getSentiments() {
    console.log("fetch sentiments data from backend")
    // fetch a big object from server, with keys being category names
    fetch("/api/sentiments", {
      method: "GET",
      cache: "no-cache",
      headers: {
        "Content-type": "application/json"
      },
      redirect: "follow"
    })
      .then(res => res.json())
      .then(res => {
        console.log(res.sentiments);
        this.setState({
          sentiment_list: res.sentiments
        });
      });
  }

  render() {
    console.log("main render");

    return (
      <div
        style={{
          width: "100%",
          height: "100%"
        }}
        id="main-div"
      >
        <Sidebar
          sidebar={this.childSideBar}
          // open={this.state.sidebar_open}
          styles={this.sideBarStyle}
          // onMouseLeave={() => this.setSidebarClosed()}
          id="switch"
          docked={true}
        >
          <Sidebar
            sidebar={this.parentSideBar}
            open={this.state.sidebar_open}
            onSetOpen={() => this.setSidebarOpen()}
            styles={this.sideBarStyle}
            // onMouseLeave={() => this.setSidebarClosed()}
            id="navigate"
          >
            <div
              style={{
                float: "right",
                height: "100%",
                width: "100%"
              }}
              id="right-contents"
            >
              <WordCloud
                onWordClick={text => this.activateTrend(text)}
                words={this.state.words}
                ver={this.state.word_list_version}
                style={{
                  height: "100%",
                  width: "100%"
                }}
                id="word-cloud"
              />
              <Trend
                enable={this.state.trend_open}
                text={this.state.overlay_text}
                handleClose={() => {
                  this.deactivateTrend();
                }}
                currentTrend={this.state.current_trend}
              />
              <Newslist />
              <Sentiments id="sentiments" sentiment_list={this.state.sentiment_list} />
            </div>
          </Sidebar>
        </Sidebar>
      </div>
    );
  }
}

ReactDOM.render(<Main />, document.getElementById("root"));
