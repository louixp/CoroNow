import React from "react";
import "./index.css";
import "./style/nav.css";

class Nav extends React.Component {
  // props: mouseOverHandler, mouseOutHandler
  constructor(props) {
    super(props);
    this.state = {
      state: "init" // state: init, expanded
    };
  }

  getScrollCallBack(id) {
    return ()=>{
      let el = document.getElementById(id);
      if (el) {
        el.scrollIntoView(true);
      }
      this.props.callbacks.closeNav();
    };
  }

  render() {
    return (
      <div
        onMouseLeave={this.props.onMouseLeave}
        style={this.props.style}
      >
        <p>this is nav bar</p>
        {/* <NavItem text="WORD CLOUD" callback={this.getScrollCallBack("word-cloud")} />
        <NavItem text="SEARCH NEWS" callback={this.getScrollCallBack("news-search")} />
        <NavItem text="SENTIMENTS" callback={this.getScrollCallBack("sentiments")} /> */}
        {this.props.items.map(el => {
          console.log("return a nav item!");
          return (<NavItem text={el.text} callback={this.getScrollCallBack(el.id)} />);
        })}
      </div>
    );
  }
}

function NavItem({text, callback}) {
  return (
  <p 
    onClick={callback}
    className="nav-item"
  >
    {text}
  </p>);
}

export default Nav;
