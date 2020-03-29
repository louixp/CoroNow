import React from "react";
import "./index.css";
import CanvasJSReact from "./lib/canvasjs.react";

var CanvasJSChart = CanvasJSReact.CanvasJSChart;

class Wordtrend extends React.Component {
  render() {
    const data = {
      word: "Good",
      frequency: [
        {
          date: [2020, 10, 2, 1],
          value: 10
        },
        { date: [2020, 10, 2, 2], value: 10 },
        { date: [2020, 10, 2, 3], value: 11 },
        { date: [2020, 10, 2, 4], value: 12 }
      ]
    };
    var frequency_arr = [];
    for (let i = 0; i < data.frequency.length; i++) {
      var freq = data.frequency[i];
      frequency_arr.push({
        x: new Date(freq.date[0], freq.date[1] - 1, freq.date[2], freq.date[3]),
        y: freq.value
      });
    }
    console.log(frequency_arr);
    const options = {
      animationEnabled: true,
      title: {
        text: "Trend for word: " + data.word
      },
      backgroundColor: "pink",
      axisX: {
        valueFormatString: "MMM.DD HH:00",
        lineThickness: 4
      },
      axisY: {
        title: "Frequency",
        includeZero: false
      },
      data: [
        {
          type: "spline",
          dataPoints: frequency_arr
        }
      ]
    };
    return (
      <div className="word_trend">
        <div className="word_trend_title">{this.props.word}</div>
        <div className="word_trend_graph">
          <CanvasJSChart options={options} />
        </div>
      </div>
    );
  }
}

export default Wordtrend;
