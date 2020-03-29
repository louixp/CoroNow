import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import "bootstrap/dist/css/bootstrap.css"; // this file is required for Modal to work
import WordCloud from "./wordcloud.js";
import Trend from "./trend.js";
import Newslist from "./newslist.js";
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
      words: []
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
    <div
      className="parent-side-bar"
      onMouseLeave={() => this.setSidebarClosed()}
      style={{
        height: "100%",
        width: "100%"
      }}
    >
      <p>this is parent side bar</p>
    </div>
  );

  // callback function for word clicking, display a trend overlay window
  activateTrend(text) {
    // fetch data here
    if (this.state.trend_open === false) {
      this.setState({
        trend_open: true,
        overlay_text: text
        // add more data to pass in here
      });
    }
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
        {/* <Sidebar
          sidebar={this.parentSideBar}
          open={this.state.sidebar_open}
          onSetOpen={() => this.setSidebarOpen()}
          styles={this.sideBarStyle}
          // onMouseLeave={() => this.setSidebarClosed()}
          id="navigate"
        > */}
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
            >
              <WordCloud
                onWordClick={text => this.activateTrend(text)}
                words={this.state.words}
                ver={this.state.word_list_version}
                style={{
                  height: "100%",
                  width: "100%"
                }}
              />
              <Trend
                enable={this.state.trend_open}
                text={this.state.overlay_text}
                handleClose={() => {
                  this.deactivateTrend();
                }}
              />
              <Newslist />
            </div>
          </Sidebar>
        </Sidebar>
      </div>
    );
  }
}

ReactDOM.render(<Main />, document.getElementById("root"));
