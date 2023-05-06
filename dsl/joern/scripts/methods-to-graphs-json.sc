import io.shiftleft.semanticcpg.dotgenerator.{AstGenerator, CdgGenerator, CfgGenerator, DotSerializer}
import io.joern.dataflowengineoss.dotgenerator.DdgGenerator
import io.shiftleft.semanticcpg.dotgenerator.DotSerializer.Graph
import scala.collection.immutable.{Map => ImmuMap}
import scala.collection.mutable.{Map => MuMap}
import scala.collection.immutable.HashSet
import io.shiftleft.codepropertygraph.generated.nodes._
import io.shiftleft.semanticcpg.language._
import io.shiftleft.semanticcpg.utils.MemberAccess
import io.circe.Json
import io.circe.syntax._
import cats.syntax.either._
import io.circe._, io.circe.parser._ 

/**
* stringRepr and toCfgNode are taken from the original codepropertygraph code base
* https://github.com/ShiftLeftSecurity/codepropertygraph/blob/master/semanticcpg/src/main/scala/io/shiftleft/semanticcpg/dotgenerator/DotSerializer.scala
*/

def stringRepr(vertex: StoredNode): String = {
    vertex match {
      case call: Call               => (call.name, call.code).toString
      case expr: Expression         => (expr.label, expr.code, toCfgNode(expr).code).toString
      case method: Method           => (method.label, method.name).toString
      case ret: MethodReturn        => (ret.label, ret.typeFullName).toString
      case param: MethodParameterIn => ("PARAM", param.code).toString
      case local: Local             => (local.label, s"${local.code}: ${local.typeFullName}").toString
      case target: JumpTarget       => (target.label, target.name).toString
      case modifier: Modifier       => ("MODIFIER", modifier.modifierType).toString()
      case _                        => ""
    }
  }

def toCfgNode(node: StoredNode): CfgNode = {
    node match {
      case node: Identifier         => node.parentExpression.get
      case node: MethodRef          => node.parentExpression.get
      case node: Literal            => node.parentExpression.get
      case node: MethodParameterIn  => node.method
      case node: MethodParameterOut => node.method.methodReturn
      case node: Call if MemberAccess.isGenericMemberAccessName(node.name) =>
        node.parentExpression.get
      case node: CallRepr     => node
      case node: MethodReturn => node
      case node: Expression   => node
    }
  }

def nodes_mapper(n: StoredNode): ImmuMap[String, String] = {
       Map("id" -> n.id.toString, "type" -> n.label, "label" -> stringRepr(n), "order" -> n.propertiesMap.get("ORDER").toString).toMap
    } 

def edges_mapper(edge: io.shiftleft.semanticcpg.dotgenerator.DotSerializer.Edge): ImmuMap[String, String] = {
       Map("key" -> edge.src.id.toString.concat("_").concat(edge.dst.id.toString).concat(edge.edgeType.toString), "source" -> edge.src.id.toString, "target" -> edge.dst.id.toString, "label" -> edge.edgeType.toString.concat(": ").concat(edge.label)).toMap
    }

def methods_mapper(m: Method): Map[String, String] = {
       Map("id" -> m.id.toString ,"fullName" ->  m.fullName, "name" ->  m.name, "filename" -> m.filename).toMap
       }

@main def exec(outDir: String, baseGraphs: String) = {
   
   val ast = new AstGenerator().generate _
   val cfg = new CfgGenerator().generate _
   val ddg = new DdgGenerator().generate _
   val cdg = new CdgGenerator().generate _

  // Create the methods file
   val project_name = workspace.getActiveProject.get.projectFile.name
   cpg.method.l.filter(m => (m.filename != "<empty>" && !m.isExternal)).map(methods_mapper).map(m => m.asJson).asJson.toString |> outDir+"/"+project_name+"_methods.json"

   val ids: List[Long] = cpg.method.filter(m => (m.filename != "<empty>" && !m.isExternal)).map(m => m.id).l

   val gen_map = MuMap("ast" -> ast, "cfg" -> cfg, "ddg" -> ddg, "cdg" -> cdg)
   val base_graphs: Array[String] = baseGraphs.split('_')
   val base_graphs_set = HashSet() ++ base_graphs

   for(id <- ids) {
       var method = cpg.method.id(id).l(0)
       var method_name = method.propertiesMap.get("NAME").toString
       var iter = base_graphs_set.iterator
       var composite_graph: Graph = null
       var base_graph_name = iter.next()

       if (base_graph_name == "pdg") {
               composite_graph = gen_map("ddg")(method) ++ gen_map("cdg")(method)
           } else {
               composite_graph = gen_map(base_graph_name)(method)
        }

       while(iter.hasNext) {
           base_graph_name = iter.next()
           if (base_graph_name == "pdg") {
               composite_graph = composite_graph ++ gen_map("ddg")(method) ++ gen_map("cdg")(method)
           } else {
               composite_graph = composite_graph ++ gen_map(base_graph_name)(method)
           }
           
       }
       val e_json = composite_graph.edges.map(edges_mapper).map(n => n.asJson).asJson 
       val v_json = composite_graph.vertices.map(nodes_mapper).map(n => n.asJson).asJson 

       Map("directed" -> true.asJson, "multigraph" -> true.asJson, "graph" -> Map("name" -> method_name.asJson).asJson  , "nodes" -> v_json, "links" -> e_json).asJson.toString |> outDir+"/"+method.name+"_"+id+"_base.json"

   }
   // close(workspace.projectByCpg(cpg).map(_.name).get)

}