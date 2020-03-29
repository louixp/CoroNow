import React from "react";
import "./index.css";
import Sidebar from "react-sidebar";
import "./style/nav.css";
import hover_menu from "./resources/hover_menu.png";

class Nav extends React.Component {
  // props: mouseOverHandler, mouseOutHandler
  constructor(props) {
    super(props);
    this.state = {
      state: "init" // state: init, expanded
    };
  }

  setSidebarOpen() {
    this.setState({
      state: "expanded"
    });
  }

  setSidebarClosed() {
    this.setState({
      state: "init"
    });
  }

  sideBarContents = (
    <div
      className="side-bar-content"
      onMouseLeave={() => this.setSidebarClosed()}
    >
      <p>hello this is nav</p>
    </div>
  );

  sideBarStyle = {
    sidebar: {
      background: "white",
    }
  }

  render() {
    let is_open = this.state.state === "expanded";
    return (
      <Sidebar
        sidebar={this.sideBarContents}
        open={is_open}
        onSetOpen={() => this.setSidebarOpen()}
        styles={this.sideBarStyle}
        onMouseLeave={() => this.setSidebarClosed()}
      >
        <img
          width="2%"
          src={hover_menu}
          alt="menu"
          onMouseOver={() => this.setSidebarOpen()}
        />
      </Sidebar>
    );
  }
}

export default Nav;
