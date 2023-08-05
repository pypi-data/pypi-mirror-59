import React from 'react';
import PropTypes from 'prop-types';
import {omit} from 'ramda';
import {Col as RSCol} from 'reactstrap';
import classNames from 'classnames';

const alignMap = {
  start: 'align-self-start',
  center: 'align-self-center',
  end: 'align-self-end',
  stretch: 'align-self-stretch',
  baseline: 'align-self-baseline'
};

const Col = props => {
  const {
    children,
    xs,
    width,
    align,
    className,
    loading_state,
    ...otherProps
  } = props;

  const alignClass = align && alignMap[align];
  const classes = classNames(className, alignClass);

  return (
    <RSCol
      xs={xs || width}
      className={classes}
      {...omit(['setProps'], otherProps)}
      data-dash-is-loading={
        (loading_state && loading_state.is_loading) || undefined
      }
    >
      {children}
    </RSCol>
  );
};

const stringOrNumberProp = PropTypes.oneOfType([
  PropTypes.number,
  PropTypes.string
]);
const columnProps = PropTypes.oneOfType([
  PropTypes.string,
  PropTypes.number,
  PropTypes.bool,
  PropTypes.shape({
    size: PropTypes.oneOfType([
      PropTypes.bool,
      PropTypes.number,
      PropTypes.string
    ]),
    // example size values:
    // 12 || "12" => col-12 or col-`width`-12
    // auto => col-auto or col-`width`-auto
    // true => col or col-`width`
    order: stringOrNumberProp,
    offset: stringOrNumberProp
  })
]);

Col.propTypes = {
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
   * Specify the width of the column. Behind the scenes this sets behaviour at
   * the xs breakpoint, and will be overriden if xs is specified.
   *
   * Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
   * dictionary with keys 'offset', 'order', 'size'. See the documentation for
   * more details.
   */
  width: columnProps,

  /**
   * Specify column behaviour on an extra small screen.
   *
   * Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
   * dictionary with keys 'offset', 'order', 'size'. See the documentation for
   * more details.
   */
  xs: columnProps,

  /**
   * Specify column behaviour on a small screen.
   *
   * Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
   * dictionary with keys 'offset', 'order', 'size'. See the documentation for
   * more details.
   */
  sm: columnProps,

  /**
   * Specify column behaviour on a medium screen.
   *
   * Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
   * dictionary with keys 'offset', 'order', 'size'. See the documentation for
   * more details.
   */
  md: columnProps,

  /**
   * Specify column behaviour on a large screen.
   *
   * Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
   * dictionary with keys 'offset', 'order', 'size'. See the documentation for
   * more details.
   */
  lg: columnProps,

  /**
   * Specify column behaviour on an extra large screen.
   *
   * Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
   * dictionary with keys 'offset', 'order', 'size'. See the documentation for
   * more details.
   */
  xl: columnProps,

  /**
   * Set vertical alignment of this column's content in the parent row. Options
   * are 'start', 'center', 'end', 'stretch', 'baseline'.
   */
  align: PropTypes.oneOf(['start', 'center', 'end', 'stretch', 'baseline']),

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
  })
};

export default Col;
