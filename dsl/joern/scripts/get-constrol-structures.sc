import scala.collection.mutable.{Map => MuMap}
import io.circe.Json
import io.circe.syntax._
import cats.syntax.either._
import io.circe._, io.circe.parser._ 
import java.io.File

def controlStructuresFinder(m: Method, csTypesArray: List[String]): MuMap[String, List[Integer]] = {
	   //val csMap = MuMap[String, List[Any]]("method_id" -> List(m.id), "method_name" -> List(m.fullName), "file_name" -> List(m.filename));
	   val filename = m.file.l(0).name
	   val csMap = MuMap[String, List[Integer]](filename -> List[Integer]());
       for (csType <- csTypesArray) {
	   	// Get all nodes of control structure type csType (e.g all If nodes)

	   	val csTypeNodes = m.controlStructure.l.filter(_.controlStructureType.equalsIgnoreCase(csType.trim())).l; 
	   	// Get all line numbers of their AST children (i.e. line numbers of statements in the control structure block)
		// e.g: csTNChildNodesLNbrs = [[1, 5, 8], [12, 78, 80], [90, 101], [115]].flatten = [1, 5, 8, 12, 78, 80, 90, 101, 115]
	   	val csTNChildNodesLNbrs = csTypeNodes.map(csn => csn.ast.lineNumber.l.dedup.l).l.flatten;
	 	csMap.get(filename) match {
			case Some(xs:List[Integer]) => csMap.update(filename, xs :++ csTNChildNodesLNbrs)
			case None => csMap
		} 
	   }
	   
	   csMap;
	   
}

@main def exec(csTypes: String, output: String) = {
    val _csTypes: List[String] = csTypes.split(',').toList;
    val methods = cpg.method.filter(m => (m.filename != "<empty>" && !m.isExternal));
    val result = methods.map(m => controlStructuresFinder(m, _csTypes));
	val filePath = new File(output,"control_structures.json").getPath;
    (result.toList.filter(_.size!=0).map(_.toSeq) reduce (_++_)).groupBy(_._1).mapValues(_.map(_._2).toList.flatten).toMap.asJson.toString |> filePath;

}