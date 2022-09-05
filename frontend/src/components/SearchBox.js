import React, { useState } from "react";
import { Button, Form, InputGroup } from "react-bootstrap";
import { useHistory } from "react-router-dom";

function SearchBox() {
  const [keyword, setKeyword] = useState("");
  let history = useHistory();

  const submitHandler = (e) => {
    e.preventDefault();
    if (keyword) {
      history.push(`/?keyword=${keyword}`);
    } else {
      history.push(history.location.pathname);
    }
  };

  return (
    <Form onSubmit={submitHandler} inline>
      <InputGroup>
        <Form.Control
          type="text"
          name="q"
          onChange={(e) => setKeyword(e.target.value)}
          className="me-sm-2 ms-sm-5"></Form.Control>
        <Button type="submit" variant="outline-success" className="p-2">
          Submit
        </Button>
      </InputGroup>
    </Form>
  );
}

export default SearchBox;
