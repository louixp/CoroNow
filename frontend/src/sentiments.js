import React from "react";
import CanvasJSReact from "./lib/canvasjs.react";
import "./style/sentiments.css";

let CanvasJSChart = CanvasJSReact.CanvasJSChart;

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
        <div className="font-effect-3d" id="sentiment_title">
          SENTIMENT ANALYSIS
        </div>
        <div id="sentiment_contents">
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
      let value = sen[sen.length - 1].value.toFixed(2);
      let color = "green";
      if (value < 0) color = "red";
      if (value == 0) color = "yellow";
      // display a single line
      return (
        <div
          id={this.props.id}
          onClick={() => this.expand()}
          className="sentiment_small"
          style={{
            color: color,
          }}
        >
          {cat}: {value}
        </div>
      );
    } else if (this.state.state === "show_trend") {
      // display trend of this category
      return (
        <div
          id={this.props.id}
          onClick={() => this.collapse()}
          className="sentiment_big"
        >
        <div
          id={this.props.id}
          onClick={() => this.expand()}
          className="sentiment_trend_title"
        >
          HISTORICAL SENTIMENT ABOUT {cat}
        </div>
          <SentimentTrend data={sen} category={this.props.category} />
        </div>
      );
    }
  }
}

class SentimentTrend extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    let data = this.props.data;
    let trend_graph = null;
    if (data != []) {
      let sen_arr = [];
      for (let i = 0; i < data.length; i++) {
        let sen = data[i];
        console.log(sen);
        let sen_date = sen.timestamp.split("-");
        sen_arr.push({
          x: new Date(
            parseInt(sen_date[0], 10),
            parseInt(sen_date[1], 10) - 1,
            parseInt(sen_date[2], 10),
            parseInt(sen_date[3], 10)
          ),
          y: sen.value
        });
      }
      const options = {
        animationEnabled: true,
        theme: "light1",
        // title: {
        //   text: "Sentiment trend about " + this.props.category
        // },
        axisX: {
          valueFormatString: "MMM.DD HH:00",
          lineThickness: 4
        },
        axisY: {
          includeZero: true,
          maximum: 1,
          minimum: -1
        },
        data: [
          {
            type: "spline",
            dataPoints: sen_arr
          }
        ]
      };
      trend_graph = <CanvasJSChart options={options} />;
    }
    return <div className="sentiment_trend">{trend_graph}</div>;
  }
}

export default Sentiments;
