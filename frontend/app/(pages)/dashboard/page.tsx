import AvaragePerClass from "@/components/AvaragePerClass";
import AveragePerSchool from "@/components/AveragePerSchool";
import BestStudentTable from "@/components/BestStudentTable";
import AverageTeacher from "@/components/AverageTeacher";
import React from "react";

function dashboard() {
  return (
    <>
    <div className=" grid grid-cols-2">

      <BestStudentTable/>
      <AvaragePerClass/>
      <AveragePerSchool/>
      <AverageTeacher/>
    </div>
    </>
  );
}

export default dashboard;
