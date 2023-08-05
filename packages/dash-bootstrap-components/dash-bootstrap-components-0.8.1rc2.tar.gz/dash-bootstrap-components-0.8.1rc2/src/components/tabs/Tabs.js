import React from 'react';
import PropTypes from 'prop-types';
import {omit} from 'ramda';
import classnames from 'classnames';
import {Nav, NavItem, NavLink, TabContent, TabPane} from 'reactstrap';
import {isNil} from 'ramda';

function resolveChildProps(child) {
  // This may need to change in the future if https://github.com/plotly/dash-renderer/issues/84 is addressed
  if (
    // disabled is a defaultProp (so it's always set)
    // meaning that if it's not set on child.props, the actual
    // props we want are lying a bit deeper - which means they
    // are coming from Dash
    isNil(child.props.disabled) &&
    child.props._dashprivate_layout &&
    child.props._dashprivate_layout.props
  ) {
    // props are coming from Dash
    return child.props._dashprivate_layout.props;
  } else {
    // else props are coming from React (e.g. Demo.js, or Tabs.test.js)
    return child.props;
  }
}

class Tabs extends React.Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.parseChildrenToArray = this.parseChildrenToArray.bind(this);

    const children = this.parseChildrenToArray();

    if (!this.props.active_tab) {
      const activeTab =
        children && (resolveChildProps(children[0]).tab_id || 'tab-0');
      this.state = {
        activeTab: activeTab
      };
      if (this.props.setProps) {
        this.props.setProps({
          active_tab: activeTab
        });
      }
    } else {
      this.state = {
        activeTab: this.props.active_tab
      };
    }
  }

  parseChildrenToArray() {
    if (this.props.children && !Array.isArray(this.props.children)) {
      // if dcc.Tabs.children contains just one single element, it gets passed as an object
      // instead of an array - so we put in in a array ourselves!
      return [this.props.children];
    }
    return this.props.children;
  }

  toggle(tab) {
    if (this.props.setProps) {
      if (this.props.active_tab !== tab) {
        this.props.setProps({active_tab: tab});
      }
    } else {
      if (this.state.activeTab !== tab) {
        this.setState({activeTab: tab});
      }
    }
  }

  static getDerivedStateFromProps(nextProps, prevState) {
    if (nextProps.active_tab && nextProps.active_tab != prevState.activeTab) {
      return {activeTab: nextProps.active_tab};
    } else return null;
  }

  render() {
    // ensure children is array of children
    const children = this.parseChildrenToArray();

    // create tab links by extracting labels from children
    const links =
      children &&
      children.map((child, idx) => {
        const childProps = resolveChildProps(child);
        const tabId = childProps.key || childProps.tab_id || 'tab-' + idx;
        return (
          <NavItem
            key={tabId}
            style={childProps.tab_style}
            className={childProps.tabClassName}
          >
            <NavLink
              className={classnames(childProps.labelClassName, {
                active: this.state.activeTab === tabId
              })}
              style={childProps.label_style}
              disabled={childProps.disabled}
              onClick={() => {
                if (!childProps.disabled) {
                  this.toggle(tabId);
                }
              }}
            >
              {childProps.label}
            </NavLink>
          </NavItem>
        );
      });

    // create tab content by extracting children from children
    const tabs =
      children &&
      children.map((child, idx) => {
        const childProps = resolveChildProps(child);
        const {
          children,
          tab_id,
          label,
          tab_style,
          label_style,
          tabClassName,
          labelClassName,
          loading_state,
          ...otherProps
        } = childProps;
        const tabId = tab_id || 'tab-' + idx;
        return (
          <TabPane
            tabId={tabId}
            key={tabId}
            {...omit(
              [
                'setProps',
                'persistence',
                'persistence_type',
                'persisted_props'
              ],
              otherProps
            )}
            data-dash-is-loading={
              (loading_state && loading_state.is_loading) || undefined
            }
          >
            {child}
          </TabPane>
        );
      });
    return (
      <div
        key={this.props.key}
        data-dash-is-loading={
          (this.props.loading_state && this.props.loading_state.is_loading) ||
          undefined
        }
      >
        <Nav
          id={this.props.id}
          tabs={true}
          card={this.props.card}
          className={this.props.className}
          style={this.props.style}
        >
          {links}
        </Nav>
        <TabContent activeTab={this.state.activeTab}>{tabs}</TabContent>
      </div>
    );
  }
}

Tabs.defaultProps = {
  persisted_props: ['active_tab'],
  persistence_type: 'local'}

Tabs.propTypes = {
  /**
   * The ID of this component, used to identify dash components
   * in callbacks. The ID needs to be unique across all of the
   * components in an app.
   */
  id: PropTypes.string,

  /**
   * The children of this component
   */
  children: PropTypes.node,

  /**
   * Defines CSS styles which will override styles previously set.
   */
  style: PropTypes.object,

  /**
   * Often used with CSS to style elements with common properties.
   */
  className: PropTypes.string,

  /**
   * A unique identifier for the component, used to improve
   * performance by React.js while rendering components
   * See https://reactjs.org/docs/lists-and-keys.html for more info
   */
  key: PropTypes.string,

  /**
   * The tab_id of the currently active tab. If tab_id has not been specified
   * for the active tab, this will default to tab-i, where i is the index
   * (starting from 0) of the tab.
   */
  active_tab: PropTypes.string,

  /**
   * Set to True if using tabs inside a CardHeader.
   */
  card: PropTypes.bool,

  /**
   * Object that holds the loading state object coming from dash-renderer
   */
  loading_state: PropTypes.shape({
    /**
     * Determines if the component is loading or not
     */
    is_loading: PropTypes.bool,
    /**
     * Holds which property is loading
     */
    prop_name: PropTypes.string,
    /**
     * Holds the name of the component that is loading
     */
    component_name: PropTypes.string
  }),

  /**
   * Used to allow user interactions in this component to be persisted when
   * the component - or the page - is refreshed. If `persisted` is truthy and
   * hasn't changed from its previous value, a `value` that the user has
   * changed while using the app will keep that change, as long as
   * the new `value` also matches what was given originally.
   * Used in conjunction with `persistence_type`.
   */
  persistence: PropTypes.oneOfType([
    PropTypes.bool,
    PropTypes.string,
    PropTypes.number
  ]),

  /**
   * Properties whose user interactions will persist after refreshing the
   * component or the page. Since only `value` is allowed this prop can
   * normally be ignored.
   */
  persisted_props: PropTypes.arrayOf(PropTypes.oneOf(['active_tab'])),

  /**
   * Where persisted user changes will be stored:
   * memory: only kept in memory, reset on page refresh.
   * local: window.localStorage, data is kept after the browser quit.
   * session: window.sessionStorage, data is cleared once the browser quit.
   */
  persistence_type: PropTypes.oneOf(['local', 'session', 'memory'])
};

export default Tabs;
