"use client";
import AveragePerClass from "@/components/AvaragePerClass";
import AveragePerSchool from "@/components/AveragePerSchool";
import BestStudentTable from "@/components/BestStudentTable";
import AverageTeacher from "@/components/AverageTeacher";
import React from "react";
import DistributionSchoolIA from "@/components/DistributionSchoolIA";
import DistSchoolAIMale from "@/components/DistSchoolAIMale";
import DistSchoolAIFemale from "@/components/DistSchoolAIFemale";
import { Card, Typography } from "antd";

function DashboardPage() {
  const { Title } = Typography;

  return (
    <>
      {/* Header consistente com o resto da aplicação */}
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-40">
        IMD-IA
      </header>

      {/* Container principal com background e padding */}
      <div className="bg-[#F5ECD5]  bg-cover bg-center bg-no-repeat min-h-screen w-full  pt-28 pb-50 px-4 sm:px-8">
        <main className="max-w-7xl mx-auto">
          <h1 className="font-[Jomolhari] text-5xl text-[#EEA03D] text-center mb-10">
            Dashboard do Município
          </h1>

          {/* Grid para os componentes do dashboard com espaçamento */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
            <BestStudentTable />
            <AveragePerClass />
            <AveragePerSchool />
            <AverageTeacher />
          </div>
          <Card style={{ marginTop: 16 }}>
            <Title level={3}>IA</Title>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
              <DistributionSchoolIA />
              <DistSchoolAIMale />
              <DistSchoolAIFemale />
            </div>
          </Card>
        </main>
      </div>
    </>
  );
}

export default DashboardPage;
