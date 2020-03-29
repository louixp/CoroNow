import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import "bootstrap/dist/css/bootstrap.css"; // this file is required for Modal to work
import WordCloud from "./wordcloud.js";
import Wordtrend from "./wordtrend.js";
import Newslist from "./newslist.js";
import Trend from "./trend.js";
import Sidebar from "react-sidebar";
import hover_menu from "./resources/hover_menu.png";

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
      current_trend: []
    };
    this.getWordList();
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
        console.log(res.words);
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

  sideBarContents = (
    <div
      className="side-bar-content"
      onMouseLeave={() => this.setSidebarClosed()}
      height="100%"
    >
      <p>hello this is nav</p>
    </div>
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
          sidebar={this.sideBarContents}
          open={this.state.sidebar_open}
          onSetOpen={() => this.setSidebarOpen()}
          styles={this.sideBarStyle}
          onMouseLeave={() => this.setSidebarClosed()}
          id="total"
        >
          <div>
            <img
              height="20px"
              src={hover_menu}
              alt="menu"
              onMouseOver={() => this.setSidebarOpen()}
            />
          </div>
          <WordCloud
            onWordClick={text => this.activateTrend(text)}
            words={this.state.words}
            ver={this.state.word_list_version}
            style={{
              position: "absolute",
              top: "20px",
              left: "0px",
              right: "0px",
              bottom: "0px"
            }}
          />
          <Trend
            enable={this.state.trend_open}
            text={this.state.overlay_text}
            handleClose={() => {
              this.deactivateTrend();
            }}
            currentTrend={this.state.current_trend}
          />
          {/* <Newslist /> */}
        </Sidebar>
      </div>
    );
  }
}

ReactDOM.render(<Main />, document.getElementById("root"));
