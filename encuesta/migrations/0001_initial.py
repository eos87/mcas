# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Organizacion'
        db.create_table('encuesta_organizacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('nombre_corto', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal('encuesta', ['Organizacion'])

        # Adding model 'Encuestador'
        db.create_table('encuesta_encuestador', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre_completo', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('encuesta', ['Encuestador'])

        # Adding model 'Encuesta'
        db.create_table('encuesta_encuesta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organizacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['encuesta.Organizacion'])),
            ('recolector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['encuesta.Encuestador'])),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('area_reside', self.gf('django.db.models.fields.IntegerField')()),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lugar.Departamento'])),
            ('municipio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lugar.Municipio'])),
            ('comunidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lugar.Comunidad'])),
            ('sexo', self.gf('django.db.models.fields.IntegerField')()),
            ('edad', self.gf('django.db.models.fields.IntegerField')()),
            ('escolaridad', self.gf('django.db.models.fields.IntegerField')()),
            ('estado_civil', self.gf('django.db.models.fields.IntegerField')()),
            ('no_hijas', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('no_hijos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('iglesia', self.gf('django.db.models.fields.IntegerField')()),
            ('que_iglesia', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('importancia_religion', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('encuesta', ['Encuesta'])

        # Adding model 'ViveCon'
        db.create_table('encuesta_vivecon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('encuesta', ['ViveCon'])

        # Adding model 'Familia'
        db.create_table('encuesta_familia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jefe', self.gf('django.db.models.fields.IntegerField')()),
            ('adultos', self.gf('django.db.models.fields.IntegerField')()),
            ('uno_siete', self.gf('django.db.models.fields.IntegerField')()),
            ('ocho_diesciseis', self.gf('django.db.models.fields.IntegerField')()),
            ('encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['encuesta.Encuesta'])),
        ))
        db.send_create_signal('encuesta', ['Familia'])

        # Adding M2M table for field vive_con on 'Familia'
        db.create_table('encuesta_familia_vive_con', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('familia', models.ForeignKey(orm['encuesta.familia'], null=False)),
            ('vivecon', models.ForeignKey(orm['encuesta.vivecon'], null=False))
        ))
        db.create_unique('encuesta_familia_vive_con', ['familia_id', 'vivecon_id'])

        # Adding model 'Abuso'
        db.create_table('encuesta_abuso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['Abuso'])

        # Adding model 'LugarAbuso'
        db.create_table('encuesta_lugarabuso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['LugarAbuso'])

        # Adding model 'Abusador'
        db.create_table('encuesta_abusador', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['Abusador'])

        # Adding model 'QueHacer'
        db.create_table('encuesta_quehacer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['QueHacer'])

        # Adding model 'DondeAprendio'
        db.create_table('encuesta_dondeaprendio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['DondeAprendio'])

        # Adding model 'DondeInformarse'
        db.create_table('encuesta_dondeinformarse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['DondeInformarse'])

        # Adding model 'Conocimiento'
        db.create_table('encuesta_conocimiento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conoce_ley', self.gf('django.db.models.fields.IntegerField')()),
            ('encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['encuesta.Encuesta'])),
        ))
        db.send_create_signal('encuesta', ['Conocimiento'])

        # Adding M2M table for field abuso on 'Conocimiento'
        db.create_table('encuesta_conocimiento_abuso', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conocimiento', models.ForeignKey(orm['encuesta.conocimiento'], null=False)),
            ('abuso', models.ForeignKey(orm['encuesta.abuso'], null=False))
        ))
        db.create_unique('encuesta_conocimiento_abuso', ['conocimiento_id', 'abuso_id'])

        # Adding M2M table for field lugares on 'Conocimiento'
        db.create_table('encuesta_conocimiento_lugares', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conocimiento', models.ForeignKey(orm['encuesta.conocimiento'], null=False)),
            ('lugarabuso', models.ForeignKey(orm['encuesta.lugarabuso'], null=False))
        ))
        db.create_unique('encuesta_conocimiento_lugares', ['conocimiento_id', 'lugarabuso_id'])

        # Adding M2M table for field quien_abusa on 'Conocimiento'
        db.create_table('encuesta_conocimiento_quien_abusa', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conocimiento', models.ForeignKey(orm['encuesta.conocimiento'], null=False)),
            ('abusador', models.ForeignKey(orm['encuesta.abusador'], null=False))
        ))
        db.create_unique('encuesta_conocimiento_quien_abusa', ['conocimiento_id', 'abusador_id'])

        # Adding M2M table for field que_hacer on 'Conocimiento'
        db.create_table('encuesta_conocimiento_que_hacer', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conocimiento', models.ForeignKey(orm['encuesta.conocimiento'], null=False)),
            ('quehacer', models.ForeignKey(orm['encuesta.quehacer'], null=False))
        ))
        db.create_unique('encuesta_conocimiento_que_hacer', ['conocimiento_id', 'quehacer_id'])

        # Adding M2M table for field donde_aprendio on 'Conocimiento'
        db.create_table('encuesta_conocimiento_donde_aprendio', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conocimiento', models.ForeignKey(orm['encuesta.conocimiento'], null=False)),
            ('dondeaprendio', models.ForeignKey(orm['encuesta.dondeaprendio'], null=False))
        ))
        db.create_unique('encuesta_conocimiento_donde_aprendio', ['conocimiento_id', 'dondeaprendio_id'])

        # Adding M2M table for field donde_informarse on 'Conocimiento'
        db.create_table('encuesta_conocimiento_donde_informarse', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conocimiento', models.ForeignKey(orm['encuesta.conocimiento'], null=False)),
            ('dondeinformarse', models.ForeignKey(orm['encuesta.dondeinformarse'], null=False))
        ))
        db.create_unique('encuesta_conocimiento_donde_informarse', ['conocimiento_id', 'dondeinformarse_id'])

        # Adding model 'PorqueAbuso'
        db.create_table('encuesta_porqueabuso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['PorqueAbuso'])

        # Adding model 'QuePiensa'
        db.create_table('encuesta_quepiensa', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['QuePiensa'])

        # Adding model 'QuePiensaVictima'
        db.create_table('encuesta_quepiensavictima', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['QuePiensaVictima'])

        # Adding model 'Actitud'
        db.create_table('encuesta_actitud', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('familia_ensena', self.gf('django.db.models.fields.IntegerField')()),
            ('escuela_ensena', self.gf('django.db.models.fields.IntegerField')()),
            ('encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['encuesta.Encuesta'])),
        ))
        db.send_create_signal('encuesta', ['Actitud'])

        # Adding M2M table for field porque_abuso on 'Actitud'
        db.create_table('encuesta_actitud_porque_abuso', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('actitud', models.ForeignKey(orm['encuesta.actitud'], null=False)),
            ('porqueabuso', models.ForeignKey(orm['encuesta.porqueabuso'], null=False))
        ))
        db.create_unique('encuesta_actitud_porque_abuso', ['actitud_id', 'porqueabuso_id'])

        # Adding M2M table for field que_piensa on 'Actitud'
        db.create_table('encuesta_actitud_que_piensa', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('actitud', models.ForeignKey(orm['encuesta.actitud'], null=False)),
            ('quepiensa', models.ForeignKey(orm['encuesta.quepiensa'], null=False))
        ))
        db.create_unique('encuesta_actitud_que_piensa', ['actitud_id', 'quepiensa_id'])

        # Adding M2M table for field que_piensa_victimas on 'Actitud'
        db.create_table('encuesta_actitud_que_piensa_victimas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('actitud', models.ForeignKey(orm['encuesta.actitud'], null=False)),
            ('quepiensavictima', models.ForeignKey(orm['encuesta.quepiensavictima'], null=False))
        ))
        db.create_unique('encuesta_actitud_que_piensa_victimas', ['actitud_id', 'quepiensavictima_id'])

        # Adding model 'QueHaria'
        db.create_table('encuesta_queharia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['QueHaria'])

        # Adding model 'QueHacePrevenir'
        db.create_table('encuesta_quehaceprevenir', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['QueHacePrevenir'])

        # Adding model 'ComoParticipo'
        db.create_table('encuesta_comoparticipo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['ComoParticipo'])

        # Adding model 'Practica'
        db.create_table('encuesta_practica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participa_prevenir', self.gf('django.db.models.fields.IntegerField')()),
            ('encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['encuesta.Encuesta'])),
        ))
        db.send_create_signal('encuesta', ['Practica'])

        # Adding M2M table for field que_haria on 'Practica'
        db.create_table('encuesta_practica_que_haria', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('practica', models.ForeignKey(orm['encuesta.practica'], null=False)),
            ('queharia', models.ForeignKey(orm['encuesta.queharia'], null=False))
        ))
        db.create_unique('encuesta_practica_que_haria', ['practica_id', 'queharia_id'])

        # Adding M2M table for field que_hago_prevenir on 'Practica'
        db.create_table('encuesta_practica_que_hago_prevenir', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('practica', models.ForeignKey(orm['encuesta.practica'], null=False)),
            ('quehaceprevenir', models.ForeignKey(orm['encuesta.quehaceprevenir'], null=False))
        ))
        db.create_unique('encuesta_practica_que_hago_prevenir', ['practica_id', 'quehaceprevenir_id'])

        # Adding M2M table for field como on 'Practica'
        db.create_table('encuesta_practica_como', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('practica', models.ForeignKey(orm['encuesta.practica'], null=False)),
            ('comoparticipo', models.ForeignKey(orm['encuesta.comoparticipo'], null=False))
        ))
        db.create_unique('encuesta_practica_como', ['practica_id', 'comoparticipo_id'])

        # Adding model 'LugarAtencion'
        db.create_table('encuesta_lugaratencion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['LugarAtencion'])

        # Adding model 'TipoAtencion'
        db.create_table('encuesta_tipoatencion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['TipoAtencion'])

        # Adding model 'EstadoActual'
        db.create_table('encuesta_estadoactual', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problema_comunidad', self.gf('django.db.models.fields.IntegerField')()),
            ('problema_pais', self.gf('django.db.models.fields.IntegerField')()),
            ('personas_atienden', self.gf('django.db.models.fields.IntegerField')()),
            ('donde_van', self.gf('django.db.models.fields.IntegerField')()),
            ('encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['encuesta.Encuesta'])),
        ))
        db.send_create_signal('encuesta', ['EstadoActual'])

        # Adding M2M table for field lugares on 'EstadoActual'
        db.create_table('encuesta_estadoactual_lugares', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('estadoactual', models.ForeignKey(orm['encuesta.estadoactual'], null=False)),
            ('lugaratencion', models.ForeignKey(orm['encuesta.lugaratencion'], null=False))
        ))
        db.create_unique('encuesta_estadoactual_lugares', ['estadoactual_id', 'lugaratencion_id'])

        # Adding M2M table for field tipo_atencion on 'EstadoActual'
        db.create_table('encuesta_estadoactual_tipo_atencion', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('estadoactual', models.ForeignKey(orm['encuesta.estadoactual'], null=False)),
            ('tipoatencion', models.ForeignKey(orm['encuesta.tipoatencion'], null=False))
        ))
        db.create_unique('encuesta_estadoactual_tipo_atencion', ['estadoactual_id', 'tipoatencion_id'])

        # Adding model 'QueFamilia'
        db.create_table('encuesta_quefamilia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['QueFamilia'])

        # Adding model 'QuienDebe'
        db.create_table('encuesta_quiendebe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('encuesta', ['QuienDebe'])

        # Adding model 'MensajeTransmiten'
        db.create_table('encuesta_mensajetransmiten', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('encuesta', ['MensajeTransmiten'])

        # Adding model 'RolMedio'
        db.create_table('encuesta_rolmedio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('encuesta', ['RolMedio'])

        # Adding model 'RolIglesia'
        db.create_table('encuesta_roliglesia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('encuesta', ['RolIglesia'])

        # Adding model 'RolEstado'
        db.create_table('encuesta_rolestado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('encuesta', ['RolEstado'])

        # Adding model 'RolOng'
        db.create_table('encuesta_rolong', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('encuesta', ['RolOng'])

        # Adding model 'RolEmpresa'
        db.create_table('encuesta_rolempresa', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('encuesta', ['RolEmpresa'])

        # Adding model 'Percepcion'
        db.create_table('encuesta_percepcion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conoce_abusados', self.gf('django.db.models.fields.IntegerField')()),
            ('defender', self.gf('django.db.models.fields.IntegerField')()),
            ('encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['encuesta.Encuesta'])),
        ))
        db.send_create_signal('encuesta', ['Percepcion'])

        # Adding M2M table for field que_familia on 'Percepcion'
        db.create_table('encuesta_percepcion_que_familia', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('percepcion', models.ForeignKey(orm['encuesta.percepcion'], null=False)),
            ('quefamilia', models.ForeignKey(orm['encuesta.quefamilia'], null=False))
        ))
        db.create_unique('encuesta_percepcion_que_familia', ['percepcion_id', 'quefamilia_id'])

        # Adding M2M table for field quien_debe on 'Percepcion'
        db.create_table('encuesta_percepcion_quien_debe', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('percepcion', models.ForeignKey(orm['encuesta.percepcion'], null=False)),
            ('quiendebe', models.ForeignKey(orm['encuesta.quiendebe'], null=False))
        ))
        db.create_unique('encuesta_percepcion_quien_debe', ['percepcion_id', 'quiendebe_id'])

        # Adding M2M table for field mensaje on 'Percepcion'
        db.create_table('encuesta_percepcion_mensaje', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('percepcion', models.ForeignKey(orm['encuesta.percepcion'], null=False)),
            ('mensajetransmiten', models.ForeignKey(orm['encuesta.mensajetransmiten'], null=False))
        ))
        db.create_unique('encuesta_percepcion_mensaje', ['percepcion_id', 'mensajetransmiten_id'])

        # Adding M2M table for field rol_medios on 'Percepcion'
        db.create_table('encuesta_percepcion_rol_medios', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('percepcion', models.ForeignKey(orm['encuesta.percepcion'], null=False)),
            ('rolmedio', models.ForeignKey(orm['encuesta.rolmedio'], null=False))
        ))
        db.create_unique('encuesta_percepcion_rol_medios', ['percepcion_id', 'rolmedio_id'])

        # Adding M2M table for field rol_iglesia on 'Percepcion'
        db.create_table('encuesta_percepcion_rol_iglesia', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('percepcion', models.ForeignKey(orm['encuesta.percepcion'], null=False)),
            ('roliglesia', models.ForeignKey(orm['encuesta.roliglesia'], null=False))
        ))
        db.create_unique('encuesta_percepcion_rol_iglesia', ['percepcion_id', 'roliglesia_id'])

        # Adding M2M table for field rol_estado on 'Percepcion'
        db.create_table('encuesta_percepcion_rol_estado', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('percepcion', models.ForeignKey(orm['encuesta.percepcion'], null=False)),
            ('rolestado', models.ForeignKey(orm['encuesta.rolestado'], null=False))
        ))
        db.create_unique('encuesta_percepcion_rol_estado', ['percepcion_id', 'rolestado_id'])

        # Adding M2M table for field rol_ongs on 'Percepcion'
        db.create_table('encuesta_percepcion_rol_ongs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('percepcion', models.ForeignKey(orm['encuesta.percepcion'], null=False)),
            ('rolong', models.ForeignKey(orm['encuesta.rolong'], null=False))
        ))
        db.create_unique('encuesta_percepcion_rol_ongs', ['percepcion_id', 'rolong_id'])

        # Adding M2M table for field rol_empresas on 'Percepcion'
        db.create_table('encuesta_percepcion_rol_empresas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('percepcion', models.ForeignKey(orm['encuesta.percepcion'], null=False)),
            ('rolempresa', models.ForeignKey(orm['encuesta.rolempresa'], null=False))
        ))
        db.create_unique('encuesta_percepcion_rol_empresas', ['percepcion_id', 'rolempresa_id'])


    def backwards(self, orm):
        
        # Deleting model 'Organizacion'
        db.delete_table('encuesta_organizacion')

        # Deleting model 'Encuestador'
        db.delete_table('encuesta_encuestador')

        # Deleting model 'Encuesta'
        db.delete_table('encuesta_encuesta')

        # Deleting model 'ViveCon'
        db.delete_table('encuesta_vivecon')

        # Deleting model 'Familia'
        db.delete_table('encuesta_familia')

        # Removing M2M table for field vive_con on 'Familia'
        db.delete_table('encuesta_familia_vive_con')

        # Deleting model 'Abuso'
        db.delete_table('encuesta_abuso')

        # Deleting model 'LugarAbuso'
        db.delete_table('encuesta_lugarabuso')

        # Deleting model 'Abusador'
        db.delete_table('encuesta_abusador')

        # Deleting model 'QueHacer'
        db.delete_table('encuesta_quehacer')

        # Deleting model 'DondeAprendio'
        db.delete_table('encuesta_dondeaprendio')

        # Deleting model 'DondeInformarse'
        db.delete_table('encuesta_dondeinformarse')

        # Deleting model 'Conocimiento'
        db.delete_table('encuesta_conocimiento')

        # Removing M2M table for field abuso on 'Conocimiento'
        db.delete_table('encuesta_conocimiento_abuso')

        # Removing M2M table for field lugares on 'Conocimiento'
        db.delete_table('encuesta_conocimiento_lugares')

        # Removing M2M table for field quien_abusa on 'Conocimiento'
        db.delete_table('encuesta_conocimiento_quien_abusa')

        # Removing M2M table for field que_hacer on 'Conocimiento'
        db.delete_table('encuesta_conocimiento_que_hacer')

        # Removing M2M table for field donde_aprendio on 'Conocimiento'
        db.delete_table('encuesta_conocimiento_donde_aprendio')

        # Removing M2M table for field donde_informarse on 'Conocimiento'
        db.delete_table('encuesta_conocimiento_donde_informarse')

        # Deleting model 'PorqueAbuso'
        db.delete_table('encuesta_porqueabuso')

        # Deleting model 'QuePiensa'
        db.delete_table('encuesta_quepiensa')

        # Deleting model 'QuePiensaVictima'
        db.delete_table('encuesta_quepiensavictima')

        # Deleting model 'Actitud'
        db.delete_table('encuesta_actitud')

        # Removing M2M table for field porque_abuso on 'Actitud'
        db.delete_table('encuesta_actitud_porque_abuso')

        # Removing M2M table for field que_piensa on 'Actitud'
        db.delete_table('encuesta_actitud_que_piensa')

        # Removing M2M table for field que_piensa_victimas on 'Actitud'
        db.delete_table('encuesta_actitud_que_piensa_victimas')

        # Deleting model 'QueHaria'
        db.delete_table('encuesta_queharia')

        # Deleting model 'QueHacePrevenir'
        db.delete_table('encuesta_quehaceprevenir')

        # Deleting model 'ComoParticipo'
        db.delete_table('encuesta_comoparticipo')

        # Deleting model 'Practica'
        db.delete_table('encuesta_practica')

        # Removing M2M table for field que_haria on 'Practica'
        db.delete_table('encuesta_practica_que_haria')

        # Removing M2M table for field que_hago_prevenir on 'Practica'
        db.delete_table('encuesta_practica_que_hago_prevenir')

        # Removing M2M table for field como on 'Practica'
        db.delete_table('encuesta_practica_como')

        # Deleting model 'LugarAtencion'
        db.delete_table('encuesta_lugaratencion')

        # Deleting model 'TipoAtencion'
        db.delete_table('encuesta_tipoatencion')

        # Deleting model 'EstadoActual'
        db.delete_table('encuesta_estadoactual')

        # Removing M2M table for field lugares on 'EstadoActual'
        db.delete_table('encuesta_estadoactual_lugares')

        # Removing M2M table for field tipo_atencion on 'EstadoActual'
        db.delete_table('encuesta_estadoactual_tipo_atencion')

        # Deleting model 'QueFamilia'
        db.delete_table('encuesta_quefamilia')

        # Deleting model 'QuienDebe'
        db.delete_table('encuesta_quiendebe')

        # Deleting model 'MensajeTransmiten'
        db.delete_table('encuesta_mensajetransmiten')

        # Deleting model 'RolMedio'
        db.delete_table('encuesta_rolmedio')

        # Deleting model 'RolIglesia'
        db.delete_table('encuesta_roliglesia')

        # Deleting model 'RolEstado'
        db.delete_table('encuesta_rolestado')

        # Deleting model 'RolOng'
        db.delete_table('encuesta_rolong')

        # Deleting model 'RolEmpresa'
        db.delete_table('encuesta_rolempresa')

        # Deleting model 'Percepcion'
        db.delete_table('encuesta_percepcion')

        # Removing M2M table for field que_familia on 'Percepcion'
        db.delete_table('encuesta_percepcion_que_familia')

        # Removing M2M table for field quien_debe on 'Percepcion'
        db.delete_table('encuesta_percepcion_quien_debe')

        # Removing M2M table for field mensaje on 'Percepcion'
        db.delete_table('encuesta_percepcion_mensaje')

        # Removing M2M table for field rol_medios on 'Percepcion'
        db.delete_table('encuesta_percepcion_rol_medios')

        # Removing M2M table for field rol_iglesia on 'Percepcion'
        db.delete_table('encuesta_percepcion_rol_iglesia')

        # Removing M2M table for field rol_estado on 'Percepcion'
        db.delete_table('encuesta_percepcion_rol_estado')

        # Removing M2M table for field rol_ongs on 'Percepcion'
        db.delete_table('encuesta_percepcion_rol_ongs')

        # Removing M2M table for field rol_empresas on 'Percepcion'
        db.delete_table('encuesta_percepcion_rol_empresas')


    models = {
        'encuesta.abusador': {
            'Meta': {'object_name': 'Abusador'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.abuso': {
            'Meta': {'object_name': 'Abuso'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.actitud': {
            'Meta': {'object_name': 'Actitud'},
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'escuela_ensena': ('django.db.models.fields.IntegerField', [], {}),
            'familia_ensena': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'porque_abuso': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.PorqueAbuso']", 'symmetrical': 'False'}),
            'que_piensa': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QuePiensa']", 'symmetrical': 'False'}),
            'que_piensa_victimas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QuePiensaVictima']", 'symmetrical': 'False'})
        },
        'encuesta.comoparticipo': {
            'Meta': {'object_name': 'ComoParticipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.conocimiento': {
            'Meta': {'object_name': 'Conocimiento'},
            'abuso': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.Abuso']", 'symmetrical': 'False'}),
            'conoce_ley': ('django.db.models.fields.IntegerField', [], {}),
            'donde_aprendio': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.DondeAprendio']", 'symmetrical': 'False'}),
            'donde_informarse': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.DondeInformarse']", 'symmetrical': 'False'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugares': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.LugarAbuso']", 'symmetrical': 'False'}),
            'que_hacer': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QueHacer']", 'symmetrical': 'False'}),
            'quien_abusa': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.Abusador']", 'symmetrical': 'False'})
        },
        'encuesta.dondeaprendio': {
            'Meta': {'object_name': 'DondeAprendio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.dondeinformarse': {
            'Meta': {'object_name': 'DondeInformarse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.encuesta': {
            'Meta': {'object_name': 'Encuesta'},
            'area_reside': ('django.db.models.fields.IntegerField', [], {}),
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'comunidad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Comunidad']"}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Departamento']"}),
            'edad': ('django.db.models.fields.IntegerField', [], {}),
            'escolaridad': ('django.db.models.fields.IntegerField', [], {}),
            'estado_civil': ('django.db.models.fields.IntegerField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iglesia': ('django.db.models.fields.IntegerField', [], {}),
            'importancia_religion': ('django.db.models.fields.IntegerField', [], {}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Municipio']"}),
            'no_hijas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'no_hijos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'organizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Organizacion']"}),
            'que_iglesia': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'recolector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuestador']"}),
            'sexo': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.encuestador': {
            'Meta': {'object_name': 'Encuestador'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_completo': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'encuesta.estadoactual': {
            'Meta': {'object_name': 'EstadoActual'},
            'donde_van': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugares': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['encuesta.LugarAtencion']", 'null': 'True', 'blank': 'True'}),
            'personas_atienden': ('django.db.models.fields.IntegerField', [], {}),
            'problema_comunidad': ('django.db.models.fields.IntegerField', [], {}),
            'problema_pais': ('django.db.models.fields.IntegerField', [], {}),
            'tipo_atencion': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['encuesta.TipoAtencion']", 'null': 'True', 'blank': 'True'})
        },
        'encuesta.familia': {
            'Meta': {'object_name': 'Familia'},
            'adultos': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jefe': ('django.db.models.fields.IntegerField', [], {}),
            'ocho_diesciseis': ('django.db.models.fields.IntegerField', [], {}),
            'uno_siete': ('django.db.models.fields.IntegerField', [], {}),
            'vive_con': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.ViveCon']", 'symmetrical': 'False'})
        },
        'encuesta.lugarabuso': {
            'Meta': {'object_name': 'LugarAbuso'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.lugaratencion': {
            'Meta': {'object_name': 'LugarAtencion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.mensajetransmiten': {
            'Meta': {'object_name': 'MensajeTransmiten'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'encuesta.organizacion': {
            'Meta': {'object_name': 'Organizacion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'nombre_corto': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        'encuesta.percepcion': {
            'Meta': {'object_name': 'Percepcion'},
            'conoce_abusados': ('django.db.models.fields.IntegerField', [], {}),
            'defender': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mensaje': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.MensajeTransmiten']", 'symmetrical': 'False'}),
            'que_familia': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QueFamilia']", 'symmetrical': 'False'}),
            'quien_debe': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QuienDebe']", 'symmetrical': 'False'}),
            'rol_empresas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolEmpresa']", 'symmetrical': 'False'}),
            'rol_estado': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolEstado']", 'symmetrical': 'False'}),
            'rol_iglesia': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolIglesia']", 'symmetrical': 'False'}),
            'rol_medios': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolMedio']", 'symmetrical': 'False'}),
            'rol_ongs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolOng']", 'symmetrical': 'False'})
        },
        'encuesta.porqueabuso': {
            'Meta': {'object_name': 'PorqueAbuso'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.practica': {
            'Meta': {'object_name': 'Practica'},
            'como': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['encuesta.ComoParticipo']", 'null': 'True', 'blank': 'True'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participa_prevenir': ('django.db.models.fields.IntegerField', [], {}),
            'que_hago_prevenir': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QueHacePrevenir']", 'symmetrical': 'False'}),
            'que_haria': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QueHaria']", 'symmetrical': 'False'})
        },
        'encuesta.quefamilia': {
            'Meta': {'object_name': 'QueFamilia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quehaceprevenir': {
            'Meta': {'object_name': 'QueHacePrevenir'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quehacer': {
            'Meta': {'object_name': 'QueHacer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.queharia': {
            'Meta': {'object_name': 'QueHaria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quepiensa': {
            'Meta': {'object_name': 'QuePiensa'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quepiensavictima': {
            'Meta': {'object_name': 'QuePiensaVictima'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quiendebe': {
            'Meta': {'object_name': 'QuienDebe'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.rolempresa': {
            'Meta': {'object_name': 'RolEmpresa'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.rolestado': {
            'Meta': {'object_name': 'RolEstado'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.roliglesia': {
            'Meta': {'object_name': 'RolIglesia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.rolmedio': {
            'Meta': {'object_name': 'RolMedio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.rolong': {
            'Meta': {'object_name': 'RolOng'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.tipoatencion': {
            'Meta': {'object_name': 'TipoAtencion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.vivecon': {
            'Meta': {'object_name': 'ViveCon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'lugar.comunidad': {
            'Meta': {'object_name': 'Comunidad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Municipio']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'lugar.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        'lugar.municipio': {
            'Meta': {'ordering': "['departamento__nombre']", 'object_name': 'Municipio'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Departamento']"}),
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'latitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['encuesta']
