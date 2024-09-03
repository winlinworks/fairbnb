import React from "react";
import { Input } from "../input";
import { DatePickerWithRange } from "../date-picker";

function NavSearch() {
  return (
    <>
      <Input
        type="text"
        placeholder="where are you going?"
        className="max-w-xs dark:bg-muted"
      ></Input>
      <DatePickerWithRange />
    </>
  );
}

export default NavSearch;
