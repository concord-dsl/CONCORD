import io.circe.Json
import io.circe.syntax._
import cats.syntax.either._
import io.circe._, io.circe.parser._ 
import java.io.File

def printStatements(m: Method): Map[String, List[(Integer, String)]] = {
       val printRegex: scala.util.matching.Regex = ".*print.*".r
       val nodes = m.ast.l.filter{ n => printRegex.findFirstIn(n.code).isDefined }
       Map(m.file.l(0).name -> nodes.map(x => (x.lineNumber.toList.l(0), x.code)))
}
       
@main def exec(output: String) = {
    val methods = cpg.method.filter(m => (m.filename != "<empty>" && !m.isExternal));
    val result = methods.map(printStatements);
    val filePath = new File(output,"print_stmnts.json").getPath;
    (result.toList.filter(_.size!=0).map(_.toSeq) reduce (_++_)).groupBy(_._1).mapValues(_.map(_._2).toList.flatten).toMap.asJson.toString |> filePath;

}