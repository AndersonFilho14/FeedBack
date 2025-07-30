import html2canvas from "html2canvas";
import jsPDF from "jspdf";

export const gerarPDF = async (elemento: HTMLElement | null) => {
  if (!elemento) return;

  // Captura o conteúdo como imagem (canvas)
  const canvas = await html2canvas(elemento, {
    scale: 2, // Alta resolução
    useCORS: true,
  });

  const imgData = canvas.toDataURL("image/png");

  const pdf = new jsPDF("p", "mm", "a4");
  const pdfWidth = pdf.internal.pageSize.getWidth(); // 210mm
  const pdfHeight = pdf.internal.pageSize.getHeight(); // 297mm

  const imgWidth = pdfWidth;
  const imgHeight = (canvas.height * imgWidth) / canvas.width;

  let heightLeft = imgHeight;
  let position = 0;

  // Começa na primeira página
  pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);

  // Adiciona mais páginas conforme necessário
  while (heightLeft > pdfHeight) {
    position -= pdfHeight;
    heightLeft -= pdfHeight;
    pdf.addPage();
    pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
  }

  pdf.save("relatorio-desempenho.pdf");
};
