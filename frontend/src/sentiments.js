import React from "react";
import "./style/sentiments.css";

class Sentiments extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      state: "init"
    };
  }

  render() {
    let categories = Object.keys(this.props.sentiment_list);
    return (
      <div
        style={{
          height: "100%",
          width: "100%"
        }}
        id={this.props.id}
      >
        <div>this is sentiment</div>
        {categories.map((val, ind) => {
          let sen = this.props.sentiment_list[val]; // sentiment array of the current category
          return (
            <SentimentItem
              category={val}
              sentiment_list={sen}
              id={"sentiment_" + val}
            />
          );
        })}
      </div>
    );
  }
}

class SentimentItem extends React.Component {
  constructor({ category, sentiment_list }) {
    super({ category, sentiment_list });
    this.state = {
      state: "show_last" // states: show_last, show_trend
    };
  }

  // callback function, expand this item
  expand() {
    if (this.state.state === "show_last") {
      this.setState({
        state: "show_trend"
      });
    }
  }

  // callback function to go back
  collapse() {
    if (this.state.state === "show_trend") {
      this.setState({
        state: "show_last"
      });
    }
  }

  render() {
    let cat = this.props.category;
    let sen = this.props.sentiment_list;
    if (this.state.state === "show_last") {
      // display a single line
      return (
        <div id={this.props.id} onClick={() => this.expand()}>
          {cat}: {sen[sen.length - 1].value}
        </div>
      );
    } else if (this.state.state === "show_trend") {
      // display trend of this category
      return (
        <div id={this.props.id} onClick={() => this.collapse()}>
          this item has been expanded, click to collapse
        </div>
      );
    }
  }
}

export default Sentiments;
